from datetime import datetime
import logging

from app import config
import service.part_of_day as pd
from service.image_search import ImageSearch
from app.task_manager.task import PlanningTask
from service.date_utils import get_weekday


class ImagePoster(PlanningTask):
    """
    Посылатель картинок, планируемая задача
    """
    def __init__(self, bot, chat_id, google_api_key, google_search_id):
        super().__init__(name=f"ImagePoster for chat {chat_id}")
        self.__bot = bot
        self.__chat_id = chat_id
        self.__finder = ImageSearch(google_api_key, google_search_id)
        self.__log = logging.getLogger(config.logUtils.gen_name(self))
        self._planNextRun()

    def _planNextRun(self):
        # Определяем время следующего запуска
        if config.TEST_MODE:
            self.planTime = pd.next_time(None, config.TEST_DELTA_TIME)
        else:
            self.planTime = pd.next_random_time()
        self.__log.info(f"Task {self.name}, next time to run {self.planTime}")

    async def _do(self):
        # Получаем урл картинки
        url = await self.get_image()
        # Отправляем
        if url:
            await self.__bot.send_message(self.__chat_id, message=url)

    async def get_image(self, dt: datetime = None) -> str:
        # Составить поисковую фразу
        dt_current = dt or datetime.now()
        search_template = config.PHRASES[pd.part_of_day(dt)]
        # noinspection StrFormat
        search_string = search_template.format(day_of_week=get_weekday(dt_current))
        # Найти картинку
        try:
            if search_string:
                url = self.__finder.search(search_string, count_images=20)
                return url
        except Exception as e:
            self.__log.exception(f"Error due search: {e}")
        return ""
