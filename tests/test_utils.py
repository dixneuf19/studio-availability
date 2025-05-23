from datetime import date as Date, datetime as Datetime, time as Time
from app.utils import (
    get_dates_from_range,
    strip_room_name,
    combine_datetime_midnight_aware,
    get_bookings_per_room,
)
from app.models import Booking, Room, Band


def test_get_dates_from_range():
    from_date = Date(2023, 1, 1)
    to_date = Date(2023, 1, 5)
    expected_dates = [
        Date(2023, 1, 1),
        Date(2023, 1, 2),
        Date(2023, 1, 3),
        Date(2023, 1, 4),
        Date(2023, 1, 5),
    ]
    assert get_dates_from_range(from_date, to_date) == expected_dates


def test_strip_room_name():
    assert strip_room_name("123. Room Name") == "Room Name"
    assert strip_room_name("123.Room Name") == "Room Name"
    assert strip_room_name("Room Name") == "Room Name"
    assert strip_room_name("1.Sound City") == "Sound City"
    assert strip_room_name("2.Pyramid Club (Cabine)") == "Pyramid Club (Cabine)"
    assert strip_room_name("3. John Bonham") == "John Bonham"
    assert strip_room_name("4.The Factory") == "The Factory"
    assert strip_room_name("5.Delta lab (Piano)") == "Delta lab (Piano)"
    assert strip_room_name("6.Cotton Club (Piano)") == "Cotton Club (Piano)"
    assert strip_room_name("Studio MAO") == "Studio MAO"
    assert strip_room_name("7.The Fillmore") == "The Fillmore"
    assert strip_room_name("8. Jeff Porcaro") == "Jeff Porcaro"
    assert strip_room_name("9. The Roxy (Cabine Piano)") == "The Roxy (Cabine Piano)"
    assert strip_room_name("10.Black Rock") == "Black Rock"
    assert strip_room_name("11.Webster Hall") == "Webster Hall"
    assert strip_room_name("12.Birdland ") == "Birdland"
    assert strip_room_name("13.Electric Lady ") == "Electric Lady"
    assert strip_room_name("14.Apollo Theater ") == "Apollo Theater"
    assert strip_room_name("15.Carnegie Hall ") == "Carnegie Hall"
    assert strip_room_name("16.Camden Palace (Piano)") == "Camden Palace (Piano)"
    assert strip_room_name("17.Paradise Garage (DJing)") == "Paradise Garage (DJing)"
    assert strip_room_name("18.L'Hacienda (DJing)") == "L'Hacienda (DJing)"
    assert strip_room_name("19.The Loft (DJing)") == "The Loft (DJing)"
    assert strip_room_name("20.Keith Moon (Drums)") == "Keith Moon (Drums)"
    assert strip_room_name("21.Elvin Jones (Drums)") == "Elvin Jones (Drums)"
    assert (
        strip_room_name("22.Tony Williams (Cabine Piano)")
        == "Tony Williams (Cabine Piano)"
    )
    assert (
        strip_room_name("23. Duke Ellington (Cabine Piano)")
        == "Duke Ellington (Cabine Piano)"
    )
    assert strip_room_name("Random Room") == "Random Room"
    assert strip_room_name("") == ""


def test_combine_datetime_midnight_aware():
    date = Date(2023, 1, 1)
    time_midnight = Time(0, 0)
    time_random = Time(19, 19)
    expected_midnight = Datetime(2023, 1, 2, 0, 0)
    expected_random = Datetime(2023, 1, 1, 19, 19)
    assert combine_datetime_midnight_aware(date, time_midnight) == expected_midnight
    assert combine_datetime_midnight_aware(date, time_random) == expected_random


def test_get_bookings_per_room():
    band = Band(id=1, name="Band 1")
    room1 = Room(
        id=1,
        name="Room 1",
        description="A large room",
        size=100,
        open=Time(9, 0),
        close=Time(17, 0),
        studio_name="hf-14",
    )
    room2 = Room(
        id=2,
        name="Room 2",
        description="A medium room",
        size=80,
        open=Time(9, 0),
        close=Time(17, 0),
        studio_name="hf-14",
    )
    bookings = [
        Booking(
            type=1,
            date=Date.today(),
            start=Time(10, 0),
            end=Time(11, 0),
            band=band,
            room=room1,
        ),
        Booking(
            type=1,
            date=Date.today(),
            start=Time(12, 0),
            end=Time(13, 0),
            band=band,
            room=room1,
        ),
        Booking(
            type=1,
            date=Date.today(),
            start=Time(14, 0),
            end=Time(15, 0),
            band=band,
            room=room2,
        ),
    ]

    bookings_per_room = get_bookings_per_room(bookings)

    assert len(bookings_per_room) == 2
    assert room1 in bookings_per_room
    assert room2 in bookings_per_room
    assert len(bookings_per_room[room1]) == 2
    assert len(bookings_per_room[room2]) == 1
    assert bookings_per_room[room1][0].start == Time(10, 0)
    assert bookings_per_room[room1][1].start == Time(12, 0)
    assert bookings_per_room[room2][0].start == Time(14, 0)
