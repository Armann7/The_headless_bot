from abc import abstractmethod
import logging
import asyncio
import aiohttp

from app import config


class Mouth:
    """
    Выдаем ответные реплики
    """
    @abstractmethod
    async def answer(self, phrase: str) -> str:
        ...


class MouthHTTP(Mouth):
    """
    Реплики из веб-сервиса The Bender's Mouth.
    """
    def __init__(self):
        self.__log = logging.getLogger(config.logUtils.gen_name(self))

    async def answer(self, phrase: str) -> str:
        self.__log.info(f'Phrase - {phrase}')
        url = config.URL_BENDERS_MOUTH

        text = ""
        try:
            timeout = aiohttp.ClientTimeout(total=3600)
            async with aiohttp.ClientSession() as session:
                try:
                    async with session.get(url, params={'phrase': phrase}, timeout=timeout) as response:
                        resp_json = await response.json()
                        text = resp_json["response"]
                except asyncio.TimeoutError as exc:
                    self.__log.exception(f"Timeout: {exc}")
        except Exception as exc:
            self.__log.exception(f"Error on request to {url}: {exc}")

        self.__log.info(f'Response - {text}')
        return text
