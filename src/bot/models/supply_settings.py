from sqlalchemy.orm import Mapped, mapped_column

from db import Base


class SupplySettings(Base):
    __tablename__ = "supply_settings"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    value: Mapped[int] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    short_name: Mapped[str] = mapped_column(nullable=False)
