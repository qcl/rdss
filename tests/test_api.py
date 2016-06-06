"""
Tests for rdss api.
"""

import datetime
import json

import pytest
import webapp2

import main


URL_ROOT = "/"


END_DATE_CASES = [
    (
        "2016-06-03", "2016-03-05", 0, {
        "startDate": "2016-03-05",
        "discount": 0,
        "endDate": "2019-03-05",
        "formattedRemain": {
            "date": 5,
            "month": 9,
            "year": 2
        },
        "stage": 2,
        "today": "2016-06-03",
        "passed": 90,
        "remain": 1005,
        "total": 1095,
        "success": True,
        }
    ),
    (
        "2016-06-06", "2016-02-29", 0, {
        "startDate": "2016-02-29",
        "discount": 0,
        "endDate": "2019-02-28",
        "formattedRemain": {
            "date": 27,
            "month": 8,
            "year": 2
        },
        "stage": 2,
        "today": "2016-06-06",
        "passed": 98,
        "remain": 997,
        "total": 1095,
        "success": True,
        }
    ),
]


@pytest.mark.parametrize("desired_today, startDate, discount, expected_response",
    END_DATE_CASES)
def test_endDate(monkeypatch, desired_today, startDate, discount, expected_response):
    class MockDate(datetime.date):
        @classmethod
        def today(cls):
            return datetime.date(*(int(token) for token in
                desired_today.split("-")))
    monkeypatch.setattr(datetime, "date", MockDate)
    reload(main)
    app = webapp2.WSGIApplication([(URL_ROOT, main.RDSSAPIendDateHandeler)])
    response = app.get_response(URL_ROOT +
        "?startDate={}&discount={}".format(startDate, discount))
    assert json.loads(response.body) == expected_response
