from pydantic import UUID4, Field

from api.schemas.base_model import ModelConfig


class CreateReportData(ModelConfig):
    task_id: UUID4 = Field(..., alias="taskId")


class CreateReportResponse(ModelConfig):
    data: CreateReportData = Field(...)


class CheckStatusReportData(ModelConfig):
    id: UUID4 = Field(...)
    status: str = Field(...)


class CheckStatusReportResponse(ModelConfig):
    data: CheckStatusReportData = Field(...)


class WarehouseData(ModelConfig):
    warehouse_name: str = Field(alias="warehouseName")
    quantity: int = Field(...)


class WarehouseRemainsReportData(ModelConfig):
    brand: str | None = Field(None)
    subject_name: str | None = Field(None, alias="subjectName")
    vendor_code: str | None = Field(None, alias="vendorCode")
    nm_id: int | None = Field(None, alias="nmId")
    barcode: str | None = Field(None)
    tech_size: str | None = Field(None, alias="techSize")
    volume: float | None = Field(None)
    warehouses: list[WarehouseData] = Field(None)


class WbSupplies(ModelConfig):
    name: str = Field(...)
