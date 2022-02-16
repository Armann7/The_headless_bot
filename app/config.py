import os

import config_main
from service.log_utils import LogUtils
from service.config import MORNING, MIDDAY, EVENING, NIGHT

PROJECT_ROOT = config_main.PROJECT_ROOT

# Тестовый режим. Бот стартует с рядом ограничений - только один фиксированный чат
TEST_MODE = False
TEST_MODE_CHAT_ID = {-515049808}
TEST_DELTA_TIME = 5                    # Период отработки заданий, минут

# Параметры аккаунта бота
BOT_NAME = "The headless"
BOT_TOKEN = os.environ.get('BOT_TOKEN')
API_ID = os.environ.get('API_ID')
API_HASH = os.environ.get('API_HASH')

# Связь с внешними сервисами
URL_BENDERS_MOUTH = "http://192.168.0.2:8001/api/talk"
URL_BENDERS_MOUTH_TEST = "http://127.0.0.1:8000/api/talk"
AMQP_BENDERS_MOUTH = "192.168.0.2:5672"                     # В работе

# Параметры для доступа к API гугла
GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
GOOGLE_SEARCH_ID = "817b049a984987579"  # идентификатор поисковой системы

# Разные параметры
ODDS_OF_CUT_IN = 0.1                    # Вероятность вмешаться в разговор
SCHEDULER_TIME_SLICE = 60               # Время между тактами шедулера, сек
TASK_PLAN_TIME_TOLERANCE = 60*10        # Допустимое время отклонения срока запуска (сек)

# Поисковые фразы
PHRASES = \
    {MORNING: "утро {day_of_week} смешная картинка",               # Утро
     MIDDAY: "день {day_of_week} смешная картинка",                # День
     EVENING: "вечер {day_of_week} смешная картинка",              # Вечер
     NIGHT: "ночь {day_of_week} смешная картинка"}                 # Ночь

#
LOGGER_NAME = "Bender:$name"
logUtils = LogUtils(LOGGER_NAME)
