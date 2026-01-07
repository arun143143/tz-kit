from contextvars import ContextVar
from zoneinfo import ZoneInfo

from .exceptions import InvalidTimezoneError

UTC = ZoneInfo("UTC")

_current_timezone: ContextVar[ZoneInfo] = ContextVar(
    "current_timezone",
    default=UTC,
)


def set_timezone(tz_name: str, *, strict: bool = False) -> None:
    try:
        _current_timezone.set(ZoneInfo(tz_name))
    except Exception:
        if strict:
            raise InvalidTimezoneError(timezone=tz_name)
        _current_timezone.set(UTC)


def get_timezone() -> ZoneInfo:
    return _current_timezone.get()
