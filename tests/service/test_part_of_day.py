import pytest
from datetime import datetime

from service import config
import service.part_of_day as pd


@pytest.mark.service
def test_part_of_day():
    dt = datetime(year=2021, month=10, day=22, hour=7, minute=19)
    assert config.MORNING == pd.part_of_day(dt)

    dt = datetime(year=2021, month=10, day=22, hour=12, minute=47)
    assert config.MIDDAY == pd.part_of_day(dt)

    dt = datetime(year=2021, month=10, day=22, hour=10, minute=1)
    assert pd.part_of_day(dt) == pd.MORNING


@pytest.mark.service
def test_next_part_of_day():
    dt = datetime(year=2021, month=10, day=22, hour=7, minute=19)
    assert config.MIDDAY == pd.next_part_of_day(dt)
    dt = datetime(year=2021, month=10, day=22, hour=22, minute=19)
    assert config.NIGHT == pd.next_part_of_day(dt)
    dt = datetime(year=2021, month=10, day=22, hour=16, minute=19)
    assert config.EVENING == pd.next_part_of_day(dt)


@pytest.mark.service
def test_next_random_time():
    dt = datetime(year=2021, month=10, day=22, hour=7, minute=19)
    next_pd = pd.next_part_of_day(dt)
    next_time = pd.next_random_time(dt)
    assert next_time.hour >= config.PART_OF_DAY[next_pd]["time"][0].hour
    assert next_time.hour <= config.PART_OF_DAY[next_pd]["time"][1].hour


@pytest.mark.service
def test_next_time():
    dt = datetime(year=2021, month=10, day=22, hour=7, minute=19)
    dt1 = pd.next_time(dt, 10)
    assert dt1.minute == (dt.minute + 10)


if __name__ == '__main__':
    pytest.main()
