from datetime import datetime


def get_weekday(dt: datetime) -> str:
    weekday = ["понедельник", "вторник", "среда", "четверг", "пятница", "суббота", "воскресенье"]
    return weekday[dt.weekday()]
