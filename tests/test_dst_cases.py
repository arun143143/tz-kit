from datetime import datetime, timezone

from pydantic import BaseModel

from tz_kit import LocalDateTime, set_timezone


class TestSchema(BaseModel):
    dt: LocalDateTime


def test_dst_gap_spring_forward():
    set_timezone("America/New_York")
    dt = datetime(2024, 3, 10, 2, 30)
    obj = TestSchema(dt=dt)
    assert obj.dt.tzinfo == timezone.utc


def test_dst_overlap_fall_back():
    set_timezone("America/New_York")
    dt = datetime(2024, 11, 3, 1, 30)
    obj = TestSchema(dt=dt)
    assert obj.dt.tzinfo == timezone.utc
