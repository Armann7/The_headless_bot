import pytest
from service import date_utils
import datetime


@pytest.mark.service
def test_get_weekday():
    weekday = date_utils.get_weekday(datetime.datetime(year=2021, month=10, day=21))
    assert weekday.lower() == "четверг"
    weekday = date_utils.get_weekday(datetime.datetime(year=2021, month=10, day=25))
    assert weekday.lower() == "понедельник"


if __name__ == '__main__':
    pytest.main()
