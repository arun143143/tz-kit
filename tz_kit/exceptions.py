class TimezoneError(Exception):
    """
    Base exception for all timezone-related errors.
    """

    pass


class InvalidTimezoneError(TimezoneError):
    """
    Raised when an invalid or unsupported timezone string is provided.

    Example:
        "Asia/InvalidCity"
    """

    def __init__(self, timezone: str):
        self.timezone = timezone
        super().__init__(f"Invalid timezone provided: '{timezone}'")


class MissingTimezoneError(TimezoneError):
    """
    Raised when timezone information is required but not found.
    """

    def __init__(self):
        super().__init__("Timezone information is missing")


class NaiveDatetimeError(TimezoneError):
    """
    Raised when a naive datetime is encountered where a timezone-aware
    datetime is required and auto-conversion is disabled.
    """

    def __init__(self):
        super().__init__("Naive datetime provided where timezone-aware datetime was required")
