"""Test super strptime specific features"""

from datetime import datetime
import locale

import pytest

from strpdatetime import strpdatetime

TEST_DATA = [
    ["2022-01-01 00:00:00", "%Y-%m-%d %H:%M:%S", datetime(2022, 1, 1, 0, 0, 0)],
    ["2022-01-01 00:00:00.000", "%Y-%m-%d %H:%M:%S.%f", datetime(2022, 1, 1, 0, 0, 0)],
    ["{2022}", "%{%Y%}", datetime(2022, 1, 1, 0, 0, 0)],
    ["{2022-01}", "%{%Y-%m%}", datetime(2022, 1, 1, 0, 0, 0)],
    ["{2022-1}", "%{%Y-%-m%}", datetime(2022, 1, 1, 0, 0, 0)],
    ["IMG_1234_2022_11_20.jpg", "IMG_*_%Y_%m_%d.jpg", datetime(2022, 11, 20, 0, 0, 0)],
    [
        "IMG_1234_2022_11_20.jpg",
        "IMG_{4}_%Y_%m_%d.jpg",
        datetime(2022, 11, 20, 0, 0, 0),
    ],
    [
        "IMG_1234_2022_11_20.jpg",
        "IMG_{2,}_%Y_%m_%d.jpg",
        datetime(2022, 11, 20, 0, 0, 0),
    ],
    ["IMG_1234_2022_11_20.jpg", "%Y_%m_%d.jpg$", datetime(2022, 11, 20, 0, 0, 0)],
    ["2022_11_20_2022_11_19", "%Y_%m_%d", datetime(2022, 11, 20, 0, 0, 0)],
    ["2022_11_20_2022_11_19", "^%Y_%m_%d", datetime(2022, 11, 20, 0, 0, 0)],
    ["2022_11_20_2022_11_19", "%Y_%m_%d$", datetime(2022, 11, 19, 0, 0, 0)],
    ["2022_11_20_2022 11 19", "%Y %m %d", datetime(2022, 11, 19, 0, 0, 0)],
    ["2022_11_20_2022-11-19", "%Y-%m-%d", datetime(2022, 11, 19, 0, 0, 0)],
    ["2022_11_20_2022 11 9", "%Y %m %-d", datetime(2022, 11, 9, 0, 0, 0)],
    ["IMG_1234 2022 Nov 20.jpg", "IMG_* %Y %b %d.jpg", datetime(2022, 11, 20, 0, 0, 0)],
    ["IMG_1234 2022 Nov 2.jpg", "IMG_* %Y %b %-d.jpg", datetime(2022, 11, 2, 0, 0, 0)],
    [
        "IMG_1234_2022_11_20.jpg",
        "^%Y_%m_%d|%Y_%m_%d.jpg$",
        datetime(2022, 11, 20, 0, 0, 0),
    ],
]


@pytest.mark.parametrize("string, format, expected", TEST_DATA)
def test_datetime_strptime(string, format, expected):
    """Test datetime_strptime"""
    locale.setlocale(locale.LC_ALL, "en_US.UTF-8")
    assert strpdatetime(string, format) == expected
