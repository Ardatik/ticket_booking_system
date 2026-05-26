from sqlalchemy import Integer, String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Venue(Base):
    """Место проведения (кинотеатр, театр, концертная площадка)"""

    __tablename__ = "venues"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    address: Mapped[str] = mapped_column(String(500), nullable=False)
    city: Mapped[str] = mapped_column(String(100), nullable=False)

    # Тип места: cinema, theater, concert_hall
    venue_type: Mapped[str] = mapped_column(String(50), nullable=False)

    description: Mapped[str | None] = mapped_column(Text)
    capacity: Mapped[int | None] = mapped_column(Integer)

    # Связи
    halls: Mapped[list["Hall"]] = relationship(
        back_populates="venue", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Venue {self.name} ({self.venue_type})>"


class Hall(Base):
    """Зал внутри venue (для кинотеатров/театров с несколькими залами)"""

    __tablename__ = "halls"

    id: Mapped[int] = mapped_column(primary_key=True)
    venue_id: Mapped[int] = mapped_column(ForeignKey("venues.id"), nullable=False)

    name: Mapped[str] = mapped_column(String(100), nullable=False)  # "Зал 1", "VIP зал"
    capacity: Mapped[int] = mapped_column(Integer, nullable=False)

    # Связи
    venue: Mapped["Venue"] = relationship(back_populates="halls")
    seats: Mapped[list["Seat"]] = relationship(
        back_populates="hall", cascade="all, delete-orphan"
    )
    events: Mapped[list["Event"]] = relationship(back_populates="hall")

    def __repr__(self):
        return f"<Hall {self.name} at {self.venue.name}>"
