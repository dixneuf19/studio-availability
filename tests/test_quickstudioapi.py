import pytest
from datetime import date, datetime
from app.quickstudioapi import _run_quickstudio_bookings_request, RoomBooking
import httpx


async def test_run_quickstudio_bookings_request_cache_hit(mocker):
    mock_client = mocker.AsyncMock()
    test_date = date(2023, 10, 1)
    expected_bookings = [
        RoomBooking(
            id=1,
            name="Room 1",
            description="Desc 1",
            size=10,
            open=datetime(2023, 10, 1, 9, 0),
            close=datetime(2023, 10, 1, 17, 0),
            bookings=[],
        )
    ]

    mocker.patch("app.quickstudioapi.cache", {test_date: expected_bookings})
    bookings = await _run_quickstudio_bookings_request(mock_client, test_date)
    assert bookings == expected_bookings
    mock_client.get.assert_not_called()


async def test_run_quickstudio_bookings_request_cache_miss(mocker):
    mock_client = mocker.AsyncMock()
    test_date = date(2023, 10, 1)
    response_data = [
        {
            "id": 1,
            "name": "Room 1",
            "description": "Desc 1",
            "size": 10,
            "open": "2023-10-01T09:00:00+01:00",
            "close": "2023-10-01T17:00:00+01:00",
            "bookings": [],
        }
    ]
    expected_bookings = [RoomBooking.model_validate(room) for room in response_data]

    mock_response = mocker.Mock()
    mock_response.json.return_value = response_data
    mock_client.get.return_value = mock_response

    mocker.patch("app.quickstudioapi.cache", {})
    bookings = await _run_quickstudio_bookings_request(mock_client, test_date)
    assert bookings == expected_bookings
    mock_client.get.assert_called_once_with(
        "https://www.quickstudio.com/en/studios/hf-music-studio-14/bookings",
        params={"date": test_date.isoformat()},
        headers={"Accept": "application/json"},
    )


async def test_run_quickstudio_bookings_request_http_error(mocker):
    mock_client = mocker.AsyncMock()
    test_date = date(2023, 10, 1)

    mock_response = mocker.Mock()
    mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
        "Error", request=mock_response.request, response=mock_response
    )
    mock_client.get.return_value = mock_response

    mocker.patch("app.quickstudioapi.cache", {})
    with pytest.raises(httpx.HTTPStatusError):
        await _run_quickstudio_bookings_request(mock_client, test_date)
    mock_client.get.assert_called_once_with(
        "https://www.quickstudio.com/en/studios/hf-music-studio-14/bookings",
        params={"date": test_date.isoformat()},
        headers={"Accept": "application/json"},
    )
