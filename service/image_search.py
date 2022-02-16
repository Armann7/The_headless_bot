import random
import logging
from typing import Union
from google_images_search import GoogleImagesSearch
from google_images_search.fetch_resize_save import GSImage

from service import config


class ImageSearch:
    """
    Поиск картинок через гугл
    """
    def __init__(self, google_api_key, google_search_id):
        self.__gis = GoogleImagesSearch(google_api_key, google_search_id)
        self.__log = logging.getLogger(config.logUtils.gen_name(self))
        logging.getLogger("urllib3.connectionpool").setLevel(logging.INFO)

    def search(self, query: str, count_images=20) -> str:
        """
        Поиск картинки. Выбираем одну случайную из топ count_images
        :param query:           Поисковая фраза
        :param count_images:    Сколько картинок ищем
        :return:                Url картинки
        """
        image_url = ""
        # Ищем картинки
        self.__log.info("Search phrase '%s'", query)
        _search_params = {'q': query, 'num': count_images}
        self.__gis.search(search_params=_search_params)
        # Выбираем нужную
        image = self.__select_image(self.__gis.results())
        if image:
            self.__log.info("Founded url: %s", image.url)
            image_url = image.url
        else:
            self.__log.info("Couldn't find any pictures")
        self.__gis.results().clear()
        return image_url

    def __select_image(self, images) -> Union[GSImage, None]:
        """
        Выбрать одну из картинок, проверить что это именно картинка.
        :param images:
        :return:
        """
        while len(images) > 0:
            index = random.randint(0, len(images)-1)                                # nosec
            image = images[index]
            if self.__check_image(image):
                return image
            del images[index]
        return None

    def __check_image(self, image: GSImage) -> bool:
        """
        Проверим что картинка - это именно картинка.
        :param image:
        :return:
        """
        # Берем первые 20 символов и проверяем, нет ли там заголовка HTML (некоторые результаты - это страницы)
        head = str(image.get_raw_data()[:20])
        if head.find("!DOCTYPE") < 0:
            return True
        self.__log.info("Broken image on url: %s", image.url)
        return False
