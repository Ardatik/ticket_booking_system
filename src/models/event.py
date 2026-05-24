from datetime import datetime
from enum import Enum

from sqlalchemy import DateTime, Integer, Numeric, String, Text, ForeignKey
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin


class EventType(str, Enum):
    """Типы мероприятий"""

    MOVIE = "movie"
    THEATER = "theater"
    CONCERT = "concert"


class Event(Base, TimestampMixin):
    """Базовый класс для всех мероприятий (полиморфизм через joined table inheritance)"""

    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True)

    # Дискриминатор для полиморфизма
    event_type: Mapped[EventType] = mapped_column(
        SQLEnum(EventType, native_enum=False, length=50), nullable=False
    )

    # Общие поля
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)

    # Дата и время проведения
    start_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    end_time: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    # Место проведения
    hall_id: Mapped[int] = mapped_column(nullable=False)

    # Цена базовая (для разных типов мест может быть множитель)
    base_price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)

    # Изображение афиши
    poster_url: Mapped[str | None] = mapped_column(String(500))

    # Связи
    hall: Mapped["Hall"] = relationship(back_populates="events")
    bookings: Mapped[list["Booking"]] = relationship(
        back_populates="event", cascade="all, delete-orphan"
    )

    __mapper_args__ = {
        "polymorphic_identity": "event",
        "polymorphic_on": event_type,
    }

    def __repr__(self):
        return f"<Event {self.title} at {self.start_time}>"


class MovieEvent(Event):
    """Киносеанс"""

    __tablename__ = "movie_events"

    id: Mapped[int] = mapped_column(ForeignKey("events.id"), primary_key=True)

    # Специфичные для кино поля
    director: Mapped[str | None] = mapped_column(String(255))
    duration_minutes: Mapped[int] = mapped_column(Integer, nullable=False)
    age_rating: Mapped[str] = mapped_column(
        String(10), nullable=False
    )  # 0+, 6+, 12+, 16+, 18+
    genre: Mapped[str] = mapped_column(String(100), nullable=False)
    language: Mapped[str] = mapped_column(String(50), default="ru")
    has_subtitles: Mapped[bool] = mapped_column(default=False)
    is_3d: Mapped[bool] = mapped_column(default=False)

    __mapper_args__ = {
        "polymorphic_identity": EventType.MOVIE,
    }


class TheaterEvent(Event):
    """Театральный спектакль"""

    __tablename__ = "theater_events"

    id: Mapped[int] = mapped_column(ForeignKey("events.id"), primary_key=True)

    # Специфичные для театра поля
    playwright: Mapped[str | None] = mapped_column(String(255))  # Автор пьесы
    director: Mapped[str | None] = mapped_column(String(255))
    duration_minutes: Mapped[int] = mapped_column(Integer, nullable=False)
    age_rating: Mapped[str] = mapped_column(String(10), nullable=False)
    genre: Mapped[str] = mapped_column(
        String(100), nullable=False
    )  # драма, комедия, мюзикл
    cast: Mapped[str | None] = mapped_column(Text)  # JSON или текст с актерами

    __mapper_args__ = {
        "polymorphic_identity": EventType.THEATER,
    }


class ConcertEvent(Event):
    """Концерт"""

    __tablename__ = "concert_events"

    id: Mapped[int] = mapped_column(ForeignKey("events.id"), primary_key=True)

    # Специфичные для концертов поля
    artist: Mapped[str] = mapped_column(String(255), nullable=False)
    genre: Mapped[str] = mapped_column(
        String(100), nullable=False
    )  # рок, поп, классика
    duration_minutes: Mapped[int | None] = mapped_column(Integer)

    # Для концертов часто есть зоны без фиксированных мест
    has_fixed_seats: Mapped[bool] = mapped_column(default=True)

    # Дополнительные артисты
    support_acts: Mapped[str | None] = mapped_column(Text)

    __mapper_args__ = {
        "polymorphic_identity": EventType.CONCERT,
    }
