from __future__ import annotations
from sqlalchemy import ForeignKey, String, Text, Integer


from sqlalchemy.orm import Mapped, mapped_column

from database import Base

class Device(Base):
    __tablename__ = "devices"

    serial_number: Mapped[str] = mapped_column(String, primary_key=True, index=True, )
    lat: Mapped[int] = mapped_column(Integer, nullable=False)
    long: Mapped[int] = mapped_column(Integer, nullable=False)
    type: Mapped[str] = mapped_column(Text, nullable=False)
    version: Mapped[int] = mapped_column(Integer, nullable=False)
    is_active: Mapped[bool] = mapped_column(bool, nullable=False)
