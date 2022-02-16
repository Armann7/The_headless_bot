import datetime
from service.log_utils import LogUtils


# Время суток
MORNING = "morning"
MIDDAY = "midday"
EVENING = "evening"
NIGHT = "night"

PART_OF_DAY = \
    {MORNING: {                                                 # Утро
        "time": [datetime.time(6, 0), datetime.time(9, 0)],
        "next": MIDDAY},
     MIDDAY: {                                                  # День
        "time": [datetime.time(12, 0), datetime.time(15, 0)],
        "next": EVENING},
     EVENING: {                                                 # Вечер
        "time": [datetime.time(18, 0), datetime.time(21, 0)],
        "next": NIGHT},
     NIGHT: {                                                   # Ночь
        "time": [datetime.time(0, 0), datetime.time(4, 0)],
        "next": MORNING}}


LOGGER_NAME = "Service:$name"
logUtils = LogUtils(LOGGER_NAME)
