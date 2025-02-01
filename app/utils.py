import re
from datetime import date as Date
from datetime import datetime as Datetime
from datetime import time as Time
from datetime import timedelta

from itertools import groupby

from .models import Booking, Room


def get_dates_from_range(from_date: Date, to_date: Date) -> list[Date]:
    return [
        from_date + timedelta(days=day) for day in range((to_date - from_date).days + 1)
    ]


def get_room_id(booking: Booking) -> int:
    return booking.room.id


def get_room_name(booking: Booking) -> str:
    return booking.room.name


def strip_room_name(room_name: str) -> str:
    m = re.match(r"^(\d+\.\s?)?(.+)$", room_name)
    if m:
        return m.group(2).strip()
    else:
        return room_name


def combine_datetime_midnight_aware(date: Date, time: Time) -> Datetime:
    return Datetime.combine(
        # if the end time is midnight, the date is next day
        date + timedelta(days=1) if time == Time(hour=0) else date,
        time,
    )


def get_bookings_per_room(bookings: list[Booking]) -> dict[Room, list[Booking]]:
    return {
        room: list(bookings_iter)
        for room, bookings_iter in groupby(
            sorted(bookings, key=lambda x: x.room.name), key=lambda x: x.room
        )
    }
