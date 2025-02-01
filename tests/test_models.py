from datetime import time
import pytest
from app.models import Room, Band, convert_quickstudio_response
from app.quickstudioapi import RoomBooking
import json


def test_room_hash():
    room1 = Room(
        id=1,
        name="Room 1",
        description="Desc 1",
        size=10,
        open=time(9, 0),
        close=time(17, 0),
        studio_name="Studio A",
    )
    room2 = Room(
        id=1,
        name="Room 1",
        description="Desc 1",
        size=10,
        open=time(9, 0),
        close=time(17, 0),
        studio_name="Studio A",
    )
    assert hash(room1) == hash(room2)


def test_band_hash():
    band1 = Band(id=1, name="Band 1")
    band2 = Band(id=1, name="Band 1")
    assert hash(band1) == hash(band2)


def test_convert_quickstudio_response():
    with open("tests/test_data/quickstudio_anonymized.json", "r") as file:
        data = json.load(file)

    room_bookings = [RoomBooking.model_validate(room) for room in data]
    bands, bookings, room = convert_quickstudio_response("test_studio", room_bookings)

    assert len(bands) == 74
    assert len(bookings) == 80
    assert len(room) == 24

    # TODO: Add more assertions


def test_convert_quickstudio_response_no_band_exception():
    room_booking_data = {
        "id": 1,
        "name": "Room 1",
        "description": "Desc 1",
        "size": 10,
        "open": "2023-10-01T09:00:00+01:00",
        "close": "2023-10-01T17:00:00+01:00",
        "bookings": [
            {
                "type": 1,
                "start": "2023-10-01T10:00:00+01:00",
                "end": "2023-10-01T12:00:00+01:00",
                "band": None,
            }
        ],
    }
    room_bookings = [RoomBooking.model_validate(room_booking_data)]

    with pytest.raises(
        Exception, match="Booking for room 'Room 1' has no band but has type 1"
    ):
        convert_quickstudio_response("test_studio", room_bookings)


def test_convert_quickstudio_response_booking_spans_several_days_exception():
    room_booking_data = {
        "id": 1,
        "name": "Room 1",
        "description": "Desc 1",
        "size": 10,
        "open": "2023-10-01T09:00:00+01:00",
        "close": "2023-10-01T17:00:00+01:00",
        "bookings": [
            {
                "type": 1,
                "start": "2023-10-01T10:00:00+01:00",
                "end": "2023-10-02T12:00:00+01:00",
                "band": {"id": 1, "name": "Band 1"},
            }
        ],
    }
    room_bookings = [RoomBooking.model_validate(room_booking_data)]

    with pytest.raises(
        Exception, match="booking .* spans several days which is not expected"
    ):
        convert_quickstudio_response("test_studio", room_bookings)


def test_convert_quickstudio_response_unknown_booking_type_exception():
    room_booking_data = {
        "id": 1,
        "name": "Room 1",
        "description": "Desc 1",
        "size": 10,
        "open": "2023-10-01T09:00:00+01:00",
        "close": "2023-10-01T17:00:00+01:00",
        "bookings": [
            {
                "type": 99,
                "start": "2023-10-01T10:00:00+01:00",
                "end": "2023-10-01T12:00:00+01:00",
                "band": {"id": 1, "name": "Band 1"},
            }
        ],
    }
    room_bookings = [RoomBooking.model_validate(room_booking_data)]

    with pytest.raises(Exception, match="Unknow booking type '99' for room 'Room 1'"):
        convert_quickstudio_response("test_studio", room_bookings)


if __name__ == "__main__":
    pytest.main()
