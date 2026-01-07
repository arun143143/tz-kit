import asyncio

import pytest

from tz_kit import get_timezone, set_timezone


@pytest.mark.asyncio
async def test_contextvar_isolation():
    async def worker(tz, delay):
        set_timezone(tz)
        await asyncio.sleep(delay)
        return str(get_timezone())

    results = await asyncio.gather(
        worker("Asia/Kolkata", 0.1),
        worker("America/New_York", 0.05),
        worker("Europe/London", 0.15),
    )

    assert results == [
        "Asia/Kolkata",
        "America/New_York",
        "Europe/London",
    ]
