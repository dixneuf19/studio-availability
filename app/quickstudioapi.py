import os
from datetime import date, datetime
from typing import Optional

import httpx
from cachetools import TTLCache
from sqlmodel import SQLModel

BOOKING_URL = os.getenv(
    "BOOKING_URL", "https://www.quickstudio.com/en/studios/hf-music-studio-14/bookings"
)
CACHE_TTL = int(os.getenv("CACHE_TTL", "300"))  # 5 minutes


class Band(SQLModel):
    id: int
    name: str


class Booking(SQLModel):
    type: int
    start: datetime
    end: datetime
    band: Optional[Band]


class RoomBooking(SQLModel):
    id: int
    name: str
    description: str
    size: int
    open: datetime
    close: datetime
    bookings: list[Booking]


cache = TTLCache(maxsize=100, ttl=CACHE_TTL)  # 5 minutes


async def get_quickstudio_bookings(date: date) -> list[RoomBooking]:
    # Check if the bookings for the given date are already in the cache
    if date in cache:
        return cache[date]

    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.get(
            BOOKING_URL,
            params={"date": date.isoformat()},
            headers={"Accept": "application/json"},  # Force JSON response
        )

    response.raise_for_status()
    bookings = [RoomBooking(**room) for room in response.json()]

    # Store the bookings in the cache
    cache[date] = bookings

    return bookings
