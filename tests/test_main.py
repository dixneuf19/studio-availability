from fastapi.testclient import TestClient
from datetime import datetime, date, time, timedelta

from app.models import Band, Room, Booking
from app.main import _compute_room_availabilities

from app.main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"message": "OK"}


def test_html_endpoint():
    for path in ["/", "/availabilities_form", "bookings_form"]:
        response = client.get(path)
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]


def test_get_availabilities_endpoint():
    response = client.get(
        "/availabilities",
        params={
            "studio_name": "hf-14",
            "start_date": date.today().isoformat(),
            "end_date": (date.today() + timedelta(days=1)).isoformat(),
            "from_time": time(9, 0).isoformat(),
            "to_time": time(17, 0).isoformat(),
            "days_of_week": [1, 2, 3, 4, 5],
            "min_room_size": 50,
            "min_availability_duration": 60,
        },
    )
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


def test_compute_room_availabilities():
    band = Band(id=1, name="Band 1")
    room = Room(
        id=1,
        name="Room 1",
        description="A large room",
        size=100,
        open=time(9, 0),
        close=time(17, 0),
        studio_name="hf-14",
    )
    bookings = [
        Booking(
            type=1,
            date=date.today(),
            start=time(10, 0),
            end=time(11, 0),
            band=band,
            room=room,
        )
    ]
    rooms = [room]
    date_today = date.today()
    from_time = time(9, 0)
    to_time = time(17, 0)
    min_availability_duration = timedelta(minutes=60)
    min_room_size = 50

    availabilities = _compute_room_availabilities(
        bookings,
        rooms,
        date_today,
        from_time,
        to_time,
        min_availability_duration,
        min_room_size,
    )

    assert len(availabilities) > 0
    assert availabilities[0].room_name == "Room 1"
    assert availabilities[0].start == datetime.combine(
        date_today, max(room.open, from_time)
    )
    assert availabilities[0].end == datetime.combine(
        date_today, min(room.close, to_time, bookings[0].start)
    )


def test_get_bookings_endpoint():
    response = client.get(
        "/bookings",
        params={
            "studio_name": "hf-14",
            "start_date": date.today().isoformat(),
            "end_date": (date.today() + timedelta(days=1)).isoformat(),
        },
    )
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
