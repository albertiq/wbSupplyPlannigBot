import asyncio
from datetime import datetime, timedelta
from typing import Any

from api.clients.marketplace_client import MarketplaceAnalyticsClient, MarketplaceSuppliesClient
from api.schemas.warehouse_remains import WarehouseRemainsReportData
from logger.logger import logger
from services.base import AsyncBaseService
from utils import const


class MarketplaceService(AsyncBaseService):
    def __init__(
        self, analytics_api_client: MarketplaceAnalyticsClient, supplies_api_client: MarketplaceSuppliesClient
    ):
        self.api_analytics_client = analytics_api_client
        self.api_supplies_client = supplies_api_client

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
        grouped_report_data = await self._group_report_data(report)
        for vendor_barcode, remains_info in grouped_report_data.items():
            supplies = await self._form_supplies(vendor_barcode, remains_info)
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

    async def _group_report_data(self, report: list[WarehouseRemainsReportData]) -> dict:
        result = {}
        report = [data.model_dump() for data in report]
        for product in report:
            product["warehouses"] = await self._group_warehouses(product["warehouses"], const.GROUPED_WAREHOUSES)
            key = (product["vendor_code"], product["barcode"])
            warehouses_dict = {wh["warehouse_name"]: wh["quantity"] for wh in product["warehouses"]}
            result[key] = warehouses_dict

        return result

    @staticmethod
    async def _form_supplies(vendor_barcode: tuple, remains_info: dict) -> list[dict]:
        result = []
        for warehouse in const.WAREHOUSES_LIST:
            warehouse_remains = remains_info.get(warehouse, 0)
            to_client = remains_info.get(const.WarehouseRemainsInfo.ON_THE_WAY_TO_CLIENT, 0)
            total = remains_info.get(const.WarehouseRemainsInfo.TOTAL_IN_WAREHOUSES, 0)
            quantity = 0

            if (
                (not to_client and not total)
                or (0 < to_client < 3 and total > 50)
                or (to_client > 3 and warehouse_remains > 5)
            ):
                continue

            if to_client > 3 and warehouse_remains <= 5:
                match to_client:
                    case q if q < 10:
                        quantity = 5
                    case q if 10 < q < 20:
                        quantity = 10
                    case q if q > 20:
                        quantity = 20
                result.append(
                    {
                        "vendor_code": vendor_barcode[0],
                        "barcode": vendor_barcode[1],
                        "quantity": quantity,
                        "warehouse": warehouse,
                    }
                )
        return result
