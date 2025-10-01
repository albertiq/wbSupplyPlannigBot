import asyncio
from collections import defaultdict
from datetime import datetime, timedelta
from typing import Any

from api.clients.marketplace_client import MarketplaceAnalyticsClient, MarketplaceSuppliesClient
from api.schemas.warehouse_remains import WarehouseRemainsReportData
from logger.logger import logger
from models import Warehouses
from repositories.warehouses import WarehousesRepository
from services.base import AsyncBaseService
from services.supply_settings_service import SupplySettingService
from utils import const


class MarketplaceService(AsyncBaseService):
    def __init__(
        self,
        analytics_api_client: MarketplaceAnalyticsClient,
        supplies_api_client: MarketplaceSuppliesClient,
        warehouses_repo: WarehousesRepository,
        supply_settings_service: SupplySettingService,
    ):
        self.api_analytics_client = analytics_api_client
        self.api_supplies_client = supplies_api_client
        self.warehouses_repo = warehouses_repo
        self.supply_settings_service = supply_settings_service

    async def __call__(self, *args, **kwargs) -> Any:
        return await self.plan_supplies()

    async def plan_supplies(self) -> list[dict]:
        report = await self._get_report()
        analyzed_warehouse_remains = await self._analyze_warehouse_remains(report)
        return analyzed_warehouse_remains

    async def _get_report(self) -> list[WarehouseRemainsReportData] | None:
        try:
            start_time = datetime.now()
            report_task_data = await self.api_analytics_client.create_warehouse_remains_report()

            while True:
                await asyncio.sleep(const.CreateReportConsts.CREATE_REPORT_SLEEP)
                report_status = await self.api_analytics_client.get_warehouse_remains_report_status(
                    report_task_data.data.task_id
                )
                if report_status.data.status == const.ReportStatus.DONE:
                    report_data = await self.api_analytics_client.get_warehouse_remains_report(report_status.data.id)
                    return report_data

                if (datetime.now() - start_time) > timedelta(seconds=const.CreateReportConsts.CREATE_REPORT_TIMEOUT):
                    raise TimeoutError(
                        f"Отчет не сформирован за {const.CreateReportConsts.CREATE_REPORT_TIMEOUT} секунд"
                    )

                if report_status.data.status == const.ReportStatus.PROCESSING:
                    logger.info(f"Отчет в процессе формирования. Статус: {report_status.data.status}")
                    await asyncio.sleep(const.CreateReportConsts.CREATE_REPORT_TIMEOUT)
                    continue

        except Exception as err:
            logger.exception(f"Ошибка при получении отчета по поставкам: {err}, попробуйте позже.")

    async def _analyze_warehouse_remains(self, report: list[WarehouseRemainsReportData]) -> list[dict]:
        result = []
        warehouses = await self.warehouses_repo.get_warehouses()
        grouped_report_data = await self._group_report_data(report, warehouses)
        for vendor_barcode, remains_info in grouped_report_data.items():
            supplies = await self._form_supplies(vendor_barcode, remains_info, warehouses)
            result.extend(supplies)
        return result

    @staticmethod
    async def _group_warehouses(warehouses: list[dict], groups: dict) -> list[dict]:
        merged = {category: 0 for category in groups}
        result = []

        for wh in warehouses:
            matched = False
            for category, names in groups.items():
                if wh["warehouse_name"] in names:
                    merged[category] += wh["quantity"]
                    matched = True
                    break

            if not matched:
                result.append(wh)

        for category, quantity in merged.items():
            if quantity > 0:
                result.append({"warehouse_name": category, "quantity": quantity})

        return result

    async def _group_report_data(self, report: list[WarehouseRemainsReportData], warehouses: list[Warehouses]) -> dict:
        result = {}
        report = [data.model_dump() for data in report]
        for product in report:
            product["warehouses"] = await self._group_warehouses(
                product["warehouses"], await self.get_grouped_warehouses(warehouses)
            )
            key = (product["vendor_code"], product["barcode"])
            warehouses_dict = {wh["warehouse_name"]: wh["quantity"] for wh in product["warehouses"]}
            result[key] = warehouses_dict

        return result

    async def _form_supplies(
        self, vendor_barcode: tuple, remains_info: dict, warehouses: list[Warehouses]
    ) -> list[dict]:
        result = []

        settings = await self.supply_settings_service.get_settings()
        min_to_client = settings.get(const.SupplySettings.MIN_TO_CLIENT_THRESHOLD, 3)
        max_to_client_low = settings.get(const.SupplySettings.MAX_TO_CLIENT_LOW, 10)
        max_to_client_medium = settings.get(const.SupplySettings.MAX_TO_CLIENT_MEDIUM, 20)
        warehouse_remains_threshold = settings.get(const.SupplySettings.WAREHOUSE_REMAINS_THRESHOLD, 5)
        total_threshold = settings.get(const.SupplySettings.TOTAL_THRESHOLD, 50)
        quantity_small = settings.get(const.SupplySettings.QUANTITY_SMALL, 5)
        quantity_medium = settings.get(const.SupplySettings.QUANTITY_MEDIUM, 10)
        quantity_large = settings.get(const.SupplySettings.QUANTITY_LARGE, 20)

        all_warehouses = {row.group.name if row.group else row.name for row in warehouses}
        for warehouse in all_warehouses:
            warehouse_remains = remains_info.get(warehouse, 0)
            to_client = remains_info.get(const.WarehouseRemainsInfo.ON_THE_WAY_TO_CLIENT, 0)
            total = remains_info.get(const.WarehouseRemainsInfo.TOTAL_IN_WAREHOUSES, 0)
            quantity = 0
            if (
                (not to_client and not total)
                or (0 < to_client < min_to_client and total > total_threshold)
                or (to_client > min_to_client and warehouse_remains > warehouse_remains_threshold)
            ):
                continue

            if to_client > min_to_client and warehouse_remains <= warehouse_remains_threshold:
                match to_client:
                    case q if q < max_to_client_low:
                        quantity = quantity_small
                    case q if max_to_client_low < q < max_to_client_medium:
                        quantity = quantity_medium
                    case q if q > max_to_client_medium:
                        quantity = quantity_large
                result.append(
                    {
                        "vendor_code": vendor_barcode[0],
                        "barcode": vendor_barcode[1],
                        "quantity": quantity,
                        "warehouse": warehouse,
                    }
                )
        return result

    @staticmethod
    async def get_grouped_warehouses(warehouses: list[Warehouses]) -> dict:
        grouped_wh = defaultdict(list)
        for warehouse in warehouses:
            if warehouse.group:
                grouped_wh[warehouse.group.name].append(warehouse.name)

        return dict(grouped_wh)
