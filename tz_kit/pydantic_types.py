from datetime import datetime, time, timezone
from typing import Any

from pydantic import GetCoreSchemaHandler
from pydantic_core import core_schema

from .context import get_timezone
from .exceptions import NaiveDatetimeError


class LocalDateTime(datetime):
    """
    Django-like datetime field.

    Input:
    - naive datetime → assumed request timezone → UTC
    - tz-aware datetime → normalized to UTC
    - time string (HH:MM) → today in request timezone → UTC
    - time object → today in request timezone → UTC
    """

    strict: bool = False

    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        source_type,
        handler: GetCoreSchemaHandler,
    ):
        return core_schema.no_info_plain_validator_function(cls._validate)

    @classmethod
    def _validate(cls, value: Any) -> datetime:
        tz = get_timezone()

        # 1. Handle strings and normalize common non-standard formats
        if isinstance(value, str):
            # Normalize date prefix if present (e.g., 2026:01:10 or 2026/01/10 -> 2026-01-10)
            # Support DMS format (YYYY:MM:DD HH:MM or HH:MM:SS)
            if len(value) >= 10:
                prefix = value[:10]
                if (prefix[4] in ":/" and prefix[7] in ":/") or (
                    prefix[2] in ":/" and prefix[5] in ":/"
                ):
                    # Basic normalization for common separators
                    normalized_prefix = prefix.replace(":", "-").replace("/", "-")
                    value = normalized_prefix + value[10:]

            try:
                value = datetime.fromisoformat(value)
            except ValueError:
                try:
                    value = time.fromisoformat(value)
                except ValueError:
                    raise ValueError(f"Invalid datetime or time format: '{value}'")

        # 2. Handle time objects (anchor to today in user's TZ)
        if isinstance(value, time):
            now_local = datetime.now(tz)
            value = datetime.combine(now_local.date(), value)

        # 3. Final validation for datetime
        if not isinstance(value, datetime):
            raise TypeError(f"Expected datetime, time, or ISO string, got {type(value).__name__}")

        # 4. Handle naive datetimes (Django-style)
        if value.tzinfo is None:
            if cls.strict:
                raise NaiveDatetimeError()
            value = value.replace(tzinfo=tz)

        # 5. Normalize to UTC
        return value.astimezone(timezone.utc)
