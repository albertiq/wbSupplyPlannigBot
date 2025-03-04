from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db import Base


class MenuSections(Base):
    __tablename__ = "sections"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)

    menu_categories = relationship("MenuCategories", back_populates="sections")


class MenuCategories(Base):
    __tablename__ = "menu_categories"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    section_id: Mapped[int] = mapped_column(ForeignKey("sections.id"), nullable=False)
    callback_name: Mapped[str] = mapped_column(unique=True, nullable=False)
    button_text: Mapped[str] = mapped_column(nullable=False)
    order_position: Mapped[int] = mapped_column(default=0)

    sections = relationship("MenuSections", back_populates="menu_categories")
