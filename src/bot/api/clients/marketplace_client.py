from api.clients.base_client import AsyncBaseHttpClient
from api.schemas.warehouse_remains import (
    CheckStatusReportResponse,
    CreateReportResponse,
    WarehouseRemainsReportData,
    WbSupplies,
)


class MarketplaceAnalyticsClient(AsyncBaseHttpClient):
    async def create_warehouse_remains_report(self) -> CreateReportResponse:
        params = {"groupByNm": "true", "groupBySa": "true", "groupByBarcode": "true"}
        response = await self.get("/v1/warehouse_remains", params)
        return CreateReportResponse(**response)

    async def get_warehouse_remains_report_status(self, task_id: str) -> CheckStatusReportResponse:
        response = await self.get(f"/v1/warehouse_remains/tasks/{task_id}/status")
        return CheckStatusReportResponse(**response)

    async def get_warehouse_remains_report(self, task_id: str) -> list[WarehouseRemainsReportData]:
        response = await self.get(f"/v1/warehouse_remains/tasks/{task_id}/download")
        return [WarehouseRemainsReportData(**r) for r in response]


class MarketplaceSuppliesClient(AsyncBaseHttpClient):
    async def get_wb_warehouses(self) -> list[WbSupplies]:
        response = await self.get(f"/v1/warehouses")
        return [WbSupplies(**r) for r in response]
