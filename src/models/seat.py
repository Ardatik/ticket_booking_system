from enum import Enum

from sqlalchemy import Enum as SQLEnum
from sqlalchemy import Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class SeatType(str, Enum):
    """Типы мест"""

    STANDARD = "standard"  # Обычное
    VIP = "vip"  # VIP
    BALCONY = "balcony"  # Балкон
    PARTERRE = "parterre"  # Партер
    LOGE = "loge"  # Ложа
    STANDING = "standing"  # Стоячее (для концертов)


class Seat(Base):
    """Место в зале (ряд + номер места)"""

    __tablename__ = "seats"
    __table_args__ = (
        UniqueConstraint(
            "hall_id", "row_number", "seat_number", name="unique_seat_in_hall"
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    hall_id: Mapped[int] = mapped_column(nullable=False)

    # Ряд и место
    row_number: Mapped[int] = mapped_column(Integer, nullable=False)
    seat_number: Mapped[int] = mapped_column(Integer, nullable=False)

    # Тип места
    seat_type: Mapped[SeatType] = mapped_column(
        SQLEnum(SeatType, native_enum=False, length=50),
        default=SeatType.STANDARD,
        nullable=False,
    )

    # Связи
    hall: Mapped["Hall"] = relationship(back_populates="seats")
    bookings: Mapped[list["Booking"]] = relationship(back_populates="seat")

    def __repr__(self):
        return f"<Seat Row {self.row_number}, Seat {self.seat_number}>"

    @property
    def label(self) -> str:
        """Человекочитаемое название места"""
        return f"Ряд {self.row_number}, Место {self.seat_number}"
