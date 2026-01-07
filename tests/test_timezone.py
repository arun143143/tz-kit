from datetime import datetime, time, timezone

import pytest
from pydantic import BaseModel

from tz_kit import (
    InvalidTimezoneError,
    LocalDateTime,
    NaiveDatetimeError,
    get_timezone,
    local_to_utc,
    set_timezone,
    utc_to_local,
)


class TestSchema(BaseModel):
    dt: LocalDateTime


def test_basic_timezone_conversion():
    set_timezone("Asia/Kolkata")
    naive = datetime(2024, 1, 1, 12, 0)
    obj = TestSchema(dt=naive)

    assert obj.dt.tzinfo == timezone.utc
    assert obj.dt.hour == 6
    assert obj.dt.minute == 30


def test_multiple_timezones():
    cases = [
        ("Asia/Kolkata", 6, 30),
        ("America/New_York", 17, 0),
        ("Europe/London", 12, 0),
    ]

    for tz, h, m in cases:
        set_timezone(tz)
        obj = TestSchema(dt=datetime(2024, 1, 1, 12, 0))
        assert obj.dt.hour == h
        assert obj.dt.minute == m


def test_utc_to_local_and_back():
    set_timezone("Asia/Kolkata")

    utc_dt = datetime(2024, 1, 1, 12, 0, tzinfo=timezone.utc)
    local = utc_to_local(utc_dt)

    assert local.hour == 17
    assert local.minute == 30

    back = local_to_utc(local)
    assert back == utc_dt


def test_invalid_timezone_strict():
    with pytest.raises(InvalidTimezoneError):
        set_timezone("Invalid/Timezone", strict=True)


def test_invalid_timezone_fallback():
    set_timezone("Invalid/Timezone")
    assert str(get_timezone()) == "UTC"


def test_naive_datetime_strict():
    try:
        LocalDateTime.strict = True
        with pytest.raises(NaiveDatetimeError):
            TestSchema(dt=datetime(2024, 1, 1, 12, 0))
    finally:
        LocalDateTime.strict = False


def test_time_only_string():
    set_timezone("Asia/Kolkata")
    # 10:30 Kolkata -> 05:00 UTC
    obj = TestSchema(dt="10:30")
    assert obj.dt.hour == 5
    assert obj.dt.minute == 0


def test_time_object():
    set_timezone("Asia/Kolkata")
    # 15:00 Kolkata -> 09:30 UTC
    obj = TestSchema(dt=time(15, 0))
    assert obj.dt.hour == 9
    assert obj.dt.minute == 30


def test_custom_datetime_format():
    set_timezone("Asia/Kolkata")

    # Test with ':' as separator
    # 10:56 IST -> 05:26 UTC
    obj1 = TestSchema(dt="2026:01:10 10:56")
    assert obj1.dt.year == 2026
    assert obj1.dt.month == 1
    assert obj1.dt.day == 10
    assert obj1.dt.hour == 5
    assert obj1.dt.minute == 26

    # Test DMS format with seconds
    # 10:56:30 IST -> 05:26:30 UTC
    obj3 = TestSchema(dt="2026:01:10 10:56:30")
    assert obj3.dt.second == 30
    assert obj3.dt.minute == 26

    # Test with '/' as separator
    # 15:00 IST -> 09:30 UTC
    obj2 = TestSchema(dt="2026/05/20 15:00")
    assert obj2.dt.year == 2026
    assert obj2.dt.month == 5
    assert obj2.dt.hour == 9
    assert obj2.dt.minute == 30
