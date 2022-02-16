import random
from datetime import datetime, timedelta, time
from typing import Union

from service.config import PART_OF_DAY, MORNING, MIDDAY, EVENING, NIGHT


def part_of_day(dt: datetime = None) -> str:
    """
    Часть суток
    :param dt:
    :return:
    """
    dt_current = _determine_datetime(dt)

    if PART_OF_DAY[MORNING]["time"][0] <= dt_current.time() <= PART_OF_DAY[MIDDAY]["time"][0]:
        return MORNING
    elif PART_OF_DAY[MIDDAY]["time"][0] <= dt_current.time() <= PART_OF_DAY[EVENING]["time"][0]:
        return MIDDAY
    elif PART_OF_DAY[EVENING]["time"][0] <= dt_current.time():
        return EVENING
    elif PART_OF_DAY[NIGHT]["time"][0] <= dt_current.time() <= PART_OF_DAY[MORNING]["time"][0]:
        return NIGHT
    return ""


def next_part_of_day(dt: datetime = None) -> str:
    """
    Определяем часть суток
    :param dt:
    :return:
    """
    current_part_of_day = part_of_day(dt)
    return PART_OF_DAY[current_part_of_day]["next"]


def next_random_time(dt: datetime = None) -> Union[datetime, None]:
    """
    Рандомное время следующей части суток
    :param dt:
    :return:
    """
    # Определим время суток
    dt_current = _determine_datetime(dt)
    next_pd = next_part_of_day(dt_current)
    if not next_pd:
        return None
    # Дата-время следующего времени суток
    date_next = dt_current.date()
    if next_pd == NIGHT:
        date_next = date_next + timedelta(days=1)
    # Время следующего времени суток
    begin_hour = PART_OF_DAY[next_pd]["time"][0].hour
    end_hour = PART_OF_DAY[next_pd]["time"][1].hour
    hour = random.randint(begin_hour, end_hour)   # nosec
    minute = random.randint(0, 59)                # nosec
    time_next = time(hour=hour, minute=minute)
    #
    return datetime.combine(date=date_next, time=time_next)


def next_time(dt: datetime = None, delta_min: int = 0) -> datetime:
    return _determine_datetime(dt) + timedelta(minutes=delta_min)


def _determine_datetime(dt: datetime = None) -> datetime:
    """
    Определим дату-время - либо dt, либо текущее, если dt is None
    :param dt:
    :return:
    """
    return dt if dt else datetime.now()
