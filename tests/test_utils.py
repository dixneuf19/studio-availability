from datetime import date as Date, datetime as Datetime, time as Time
from app.utils import get_dates_from_range, strip_room_name, combine_datetime_midnight_aware

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
    assert strip_room_name("22.Tony Williams (Cabine Piano)") == "Tony Williams (Cabine Piano)"
    assert strip_room_name("23. Duke Ellington (Cabine Piano)") == "Duke Ellington (Cabine Piano)"

def test_combine_datetime_midnight_aware():
    date = Date(2023, 1, 1)
    time_midnight = Time(0, 0)
    time_random = Time(19, 19)
    expected_midnight = Datetime(2023, 1, 2, 0, 0)
    expected_random = Datetime(2023, 1, 1, 19, 19)
    assert combine_datetime_midnight_aware(date, time_midnight) == expected_midnight
    assert combine_datetime_midnight_aware(date, time_random) == expected_random

