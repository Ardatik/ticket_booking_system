from datetime import datetime, timezone
from enum import Enum

from sqlalchemy import DateTime, Numeric, String, UniqueConstraint, ForeignKey
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin


class BookingStatus(str, Enum):
    """Статусы бронирования"""

    PENDING = "pending"  # Ожидает оплаты
    CONFIRMED = "confirmed"  # Оплачено
    CANCELLED = "cancelled"  # Отменено
    EXPIRED = "expired"  # Истекло время бронирования


class Booking(Base, TimestampMixin):
    """Бронирование билета"""

    __tablename__ = "bookings"
    __table_args__ = (
        # Одно место нельзя забронировать дважды на одно мероприятие
        UniqueConstraint("event_id", "seat_id", name="unique_booking_per_event_seat"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    # Связи
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    event_id: Mapped[int] = mapped_column(ForeignKey("events.id"), nullable=False)
    seat_id: Mapped[int | None] = mapped_column(
        ForeignKey("seats.id"), nullable=True
    )  # NULL для концертов без фиксированных мест

    # Статус
    status: Mapped[BookingStatus] = mapped_column(
        SQLEnum(BookingStatus, native_enum=False, length=50),
        default=BookingStatus.PENDING,
        nullable=False,
    )

    # Финансы
    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)

    # Временные метки
    booked_until: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True)
    )  # Время, до которого действует резерв (обычно 15 минут)

    paid_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    cancelled_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    # Уникальный код билета
    ticket_code: Mapped[str | None] = mapped_column(String(50), unique=True)

    # Связи
    user: Mapped["User"] = relationship(back_populates="bookings")
    event: Mapped["Event"] = relationship(back_populates="bookings")
    seat: Mapped["Seat"] = relationship(back_populates="bookings")

    def __repr__(self):
        return f"<Booking #{self.id} {self.status} for {self.event.title}>"

    @property
    def is_active(self) -> bool:
        """Активно ли бронирование"""
        return self.status in (BookingStatus.PENDING, BookingStatus.CONFIRMED)

    @property
    def is_expired(self) -> bool:
        """Истекло ли время резерва"""
        if self.status != BookingStatus.PENDING or not self.booked_until:
            return False
        # Используем timezone-aware время, чтобы не сравнивать naive и aware datetime
        return datetime.now(timezone.utc) > self.booked_until
