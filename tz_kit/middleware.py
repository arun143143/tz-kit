from starlette.middleware.base import BaseHTTPMiddleware

from .context import set_timezone


class TimezoneMiddleware(BaseHTTPMiddleware):
    """
    Reads timezone from request header (X-Timezone)
    and applies it for the request lifecycle.
    """

    async def dispatch(self, request, call_next):
        tz = request.headers.get("X-Timezone", "UTC")[:64]
        set_timezone(tz)
        return await call_next(request)
