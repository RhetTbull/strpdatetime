"""Test no regression against datetime.datetime.strptime()"""

# These tests are adapted from the Python standard library at:
# https://raw.githubusercontent.com/python/cpython/main/Lib/test/datetimetester.py

import time as _time
from datetime import datetime, timedelta

import pytest

import strpdatetime

MINUTE = timedelta(minutes=1)
HOUR = timedelta(hours=1)


def test_strptime():
    string = "2004-12-01 13:02:47.197"
    format = "%Y-%m-%d %H:%M:%S.%f"
    expected = datetime.strptime(string, format)
    got = strpdatetime.strpdatetime(string, format)
    assert type(got) == datetime
    assert expected == got

    # bpo-34482: Check that surrogates are handled properly.
    inputs = [
        ("2004-12-01\ud80013:02:47.197", "%Y-%m-%d\ud800%H:%M:%S.%f"),
        ("2004\ud80012-01 13:02:47.197", "%Y\ud800%m-%d %H:%M:%S.%f"),
        ("2004-12-01 13:02\ud80047.197", "%Y-%m-%d %H:%M\ud800%S.%f"),
    ]
    for string, format in inputs:
        expected = datetime.strptime(string, format)
        got = strpdatetime.strpdatetime(string, format)
        assert got == expected

    assert strpdatetime.strpdatetime("+0002", "%z").utcoffset() == 2 * MINUTE
    assert strpdatetime.strpdatetime("-0002", "%z").utcoffset() == -2 * MINUTE
    assert strpdatetime.strpdatetime(
        "-00:02:01.000003", "%z"
    ).utcoffset() == -timedelta(minutes=2, seconds=1, microseconds=3)

    # Only local timezone and UTC are supported
    for tzseconds, tzname in (
        (0, "UTC"),
        (0, "GMT"),
        (-_time.timezone, _time.tzname[0]),
    ):
        if tzseconds < 0:
            sign = "-"
            seconds = -tzseconds
        else:
            sign = "+"
            seconds = tzseconds
        hours, minutes = divmod(seconds // 60, 60)

        dtstr = "{}{:02d}{:02d}".format(sign, hours, minutes)
        dt = strpdatetime.strpdatetime(dtstr, "%z")
        assert dt.utcoffset() == timedelta(seconds=tzseconds)

        dtstr = "{}{:02d}{:02d} {}".format(sign, hours, minutes, tzname.lower())
        dt = strpdatetime.strpdatetime(dtstr, "%z %Z")

        assert dt.utcoffset() == timedelta(seconds=tzseconds)
        assert dt.tzname().lower() == tzname.lower()

        dtstr = "{}{:02d}{:02d} {}".format(sign, hours, minutes, tzname.upper())
        dt = strpdatetime.strpdatetime(dtstr, "%z %Z")

        assert dt.utcoffset() == timedelta(seconds=tzseconds)
        assert dt.tzname().upper() == tzname.upper()

    # Can produce inconsistent datetime
    dtstr, fmt = "+1234 UTC", "%z %Z"
    dt = strpdatetime.strpdatetime(dtstr, fmt)
    assert dt.utcoffset() == 12 * HOUR + 34 * MINUTE
    assert dt.tzname() == "UTC"

    # yet will roundtrip
    assert dt.strftime(fmt) == dtstr

    # Produce naive datetime if no %z is provided
    assert strpdatetime.strpdatetime("UTC", "%Z").tzinfo is None

    with pytest.raises(ValueError):
        strpdatetime.strpdatetime("-2400", "%z")
    with pytest.raises(ValueError):
        strpdatetime.strpdatetime("-000", "%z")
    with pytest.raises(ValueError):
        strpdatetime.strpdatetime("z", "%z")


def test_strptime_single_digit():
    # bpo-34903: Check that single digit dates and times are allowed.

    with pytest.raises(ValueError):
        # %y does require two digits.
        newdate = strpdatetime.strpdatetime(
            "01/02/3 04:05:06", "%d/%m/%y %H:%M:%S"
        )

    dt1 = datetime(2003, 2, 1, 4, 5, 6)
    dt2 = datetime(2003, 1, 2, 4, 5, 6)
    dt3 = datetime(2003, 2, 1, 0, 0, 0)
    dt4 = datetime(2003, 1, 25, 0, 0, 0)
    inputs = [
        ("%-d", "1/02/03 4:5:6", "%-d/%m/%y %-H:%-M:%-S", dt1),
        ("%-m", "01/2/03 4:5:6", "%d/%-m/%y %-H:%-M:%-S", dt1),
        ("%-H", "01/02/03 4:05:06", "%d/%m/%y %-H:%M:%S", dt1),
        ("%-M", "01/02/03 04:5:06", "%d/%m/%y %H:%-M:%S", dt1),
        ("%-S", "01/02/03 04:05:6", "%d/%m/%y %H:%M:%-S", dt1),
        ("%-j", "2/03 04am:05:06", "%-j/%y %I%p:%M:%S", dt2),
        ("%-I", "02/03 4am:05:06", "%-j/%y %-I%p:%M:%S", dt2),
        ("%w", "6/04/03", "%w/%U/%y", dt3),
        # %u requires a single digit.
        ("%-W", "6/4/2003", "%u/%-W/%Y", dt3),
        ("%-V", "6/4/2003", "%u/%-V/%G", dt4),
    ]
    for _, string, format, target in inputs:
        newdate = strpdatetime.strpdatetime(string, format)
        assert newdate == target
