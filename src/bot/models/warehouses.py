from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db import Base


class WarehouseGroups(Base):
    __tablename__ = "warehouse_groups"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)

    warehouses = relationship("Warehouses", back_populates="group")


class Warehouses(Base):
    __tablename__ = "warehouses"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)
    group_id: Mapped[int] = mapped_column(ForeignKey("warehouse_groups.id"), nullable=True)

    group = relationship("WarehouseGroups", back_populates="warehouses")
