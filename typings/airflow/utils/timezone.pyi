"""
This type stub file was generated by pyright.
"""

import datetime as dt
from typing import TYPE_CHECKING, overload

from airflow.typing_compat import Literal
from pendulum.datetime import DateTime
from pendulum.tz.timezone import FixedTimezone, Timezone

if TYPE_CHECKING: ...
_PENDULUM3 = ...
utc = ...

def is_localized(value):  # -> bool:
    """
    Determine if a given datetime.datetime is aware.

    The concept is defined in Python documentation. Assuming the tzinfo is
    either None or a proper ``datetime.tzinfo`` instance, ``value.utcoffset()``
    implements the appropriate logic.

    .. seealso:: http://docs.python.org/library/datetime.html#datetime.tzinfo
    """
    ...

def is_naive(value):  # -> bool:
    """
    Determine if a given datetime.datetime is naive.

    The concept is defined in Python documentation. Assuming the tzinfo is
    either None or a proper ``datetime.tzinfo`` instance, ``value.utcoffset()``
    implements the appropriate logic.

    .. seealso:: http://docs.python.org/library/datetime.html#datetime.tzinfo
    """
    ...

def utcnow() -> dt.datetime:
    """Get the current date and time in UTC."""
    ...

def utc_epoch() -> dt.datetime:
    """Get the epoch in the user's timezone."""
    ...

@overload
def convert_to_utc(value: None) -> None: ...
@overload
def convert_to_utc(value: dt.datetime) -> DateTime: ...
def convert_to_utc(value: dt.datetime | None) -> DateTime | None:
    """
    Create a datetime with the default timezone added if none is associated.

    :param value: datetime
    :return: datetime with tzinfo
    """
    ...

@overload
def make_aware(value: None, timezone: dt.tzinfo | None = ...) -> None: ...
@overload
def make_aware(value: DateTime, timezone: dt.tzinfo | None = ...) -> DateTime: ...
@overload
def make_aware(value: dt.datetime, timezone: dt.tzinfo | None = ...) -> dt.datetime: ...
def make_aware(
    value: dt.datetime | None, timezone: dt.tzinfo | None = ...
) -> dt.datetime | None:
    """
    Make a naive datetime.datetime in a given time zone aware.

    :param value: datetime
    :param timezone: timezone
    :return: localized datetime in settings.TIMEZONE or timezone
    """
    ...

def make_naive(value, timezone=...):  # -> datetime:
    """
    Make an aware datetime.datetime naive in a given time zone.

    :param value: datetime
    :param timezone: timezone
    :return: naive datetime
    """
    ...

def datetime(*args, **kwargs):  # -> datetime:
    """
    Wrap around datetime.datetime to add settings.TIMEZONE if tzinfo not specified.

    :return: datetime.datetime
    """
    ...

def parse(string: str, timezone=..., *, strict=...) -> DateTime:
    """
    Parse a time string and return an aware datetime.

    :param string: time string
    :param timezone: the timezone
    :param strict: if False, it will fall back on the dateutil parser if unable to parse with pendulum
    """
    ...

@overload
def coerce_datetime(v: None, tz: dt.tzinfo | None = ...) -> None: ...
@overload
def coerce_datetime(v: DateTime, tz: dt.tzinfo | None = ...) -> DateTime: ...
@overload
def coerce_datetime(v: dt.datetime, tz: dt.tzinfo | None = ...) -> DateTime: ...
def coerce_datetime(
    v: dt.datetime | None, tz: dt.tzinfo | None = ...
) -> DateTime | None:
    """
    Convert ``v`` into a timezone-aware ``pendulum.DateTime``.

    * If ``v`` is *None*, *None* is returned.
    * If ``v`` is a naive datetime, it is converted to an aware Pendulum DateTime.
    * If ``v`` is an aware datetime, it is converted to a Pendulum DateTime.
      Note that ``tz`` is **not** taken into account in this case; the datetime
      will maintain its original tzinfo!
    """
    ...

def td_format(td_object: None | dt.timedelta | float | int) -> str | None:
    """
    Format a timedelta object or float/int into a readable string for time duration.

    For example timedelta(seconds=3752) would become `1h:2M:32s`.
    If the time is less than a second, the return will be `<1s`.
    """
    ...

def parse_timezone(name: str | int) -> FixedTimezone | Timezone:
    """
    Parse timezone and return one of the pendulum Timezone.

    Provide the same interface as ``pendulum.timezone(name)``

    :param name: Either IANA timezone or offset to UTC in seconds.

    :meta private:
    """
    ...

def local_timezone() -> FixedTimezone | Timezone:
    """
    Return local timezone.

    Provide the same interface as ``pendulum.tz.local_timezone()``

    :meta private:
    """
    ...

def from_timestamp(
    timestamp: int | float, tz: str | FixedTimezone | Timezone | Literal[local] = ...
) -> DateTime:
    """
    Parse timestamp and return DateTime in a given time zone.

    :param timestamp: epoch time in seconds.
    :param tz: In which timezone should return a resulting object.
        Could be either one of pendulum timezone, IANA timezone or `local` literal.

    :meta private:
    """
    ...
