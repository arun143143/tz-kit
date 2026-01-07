from __future__ import annotations

from datetime import datetime, timezone

from .context import get_timezone


def utc_to_local(dt: datetime | None) -> datetime | None:
    """
    Converts a UTC datetime to the current context's timezone.

    If input is None, returns None.
    If input is Naive, assumes it's consistent with the target timezone (or UTC).
    """
    if dt is None:
        return None
    return dt.astimezone(get_timezone())


def local_to_utc(dt: datetime | None) -> datetime | None:
    """
    Converts a local datetime (or context timezone) to UTC.

    If input is None, returns None.
    If input is Naive, assigns the current context timezone.
    If input is Aware, converts to UTC.
    """
    if dt is None:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=get_timezone())
    return dt.astimezone(timezone.utc)
