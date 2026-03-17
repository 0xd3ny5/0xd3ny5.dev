from __future__ import annotations

import datetime

import pytz

TZ = pytz.timezone("Europe/Amsterdam")


def now() -> datetime.datetime:
    return datetime.datetime.now(tz=TZ)


def as_tz(dt: datetime.datetime) -> datetime.datetime:
    return dt.astimezone(TZ)
