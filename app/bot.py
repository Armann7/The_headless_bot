import logging
import asyncio
from dataclasses import dataclass
from typing import Any

from telethon import TelegramClient
from telethon.tl.custom import Message
from telethon import events

from app import config
from app.head import Head
from app.image_poster import ImagePoster
from app.task_manager.scheduler import Scheduler


@dataclass
class ChatInfo:
    head: Head = None
    imagePoster: ImagePoster = None


class Bender:
    # __client = None         # Клиент
    # __me = None             # Инфо о боте
    # __bot_token = None      # Токен для авторизации
    # __chats = None          # Словарь с чатами, в которых бот присутствует
    # __head = None           # То, чем думаем
    # __scheduler = None      # Шедулер
    __instance = None

    def __init__(self, name: str, api_id, api_hash, bot_token):
        if not hasattr(self, "init"):
            self.init = True
            self.__client = TelegramClient(name, api_id, api_hash)
            self.__me = None
            self.__bot_token = bot_token
            self.__chats: dict = dict()
            self.__head = Head(self)
            self.__scheduler = Scheduler()
            self.__log = logging.getLogger(config.logUtils.gen_name(self))

    def __new__(cls, name: str, api_id, api_hash, bot_token):
        """
        Релизуем синглтон
        """
        if cls.__instance is None:
            cls.__instance = super(Bender, cls).__new__(cls)
        return cls.__instance

    async def start(self):
        # Подключиться к серверу
        await self.__client.connect()
        # Войти через токен. Метод sign_in возвращает информацию о боте,
        # сразу сохраним её в __me
        self.__me = await self.__client.sign_in(bot_token=self.__bot_token)
        # Установить уровень логгирования клиента телеграма
        logging.getLogger("telethon.network.mtprotosender").\
            setLevel(logging.INFO)
        logging.getLogger("telethon.extensions.messagepacker").\
            setLevel(logging.INFO)
        # Зарегистрировать хендлеры
        self.__client.add_event_handler(self.message_handler)
        # Начать получать апдейты от Телеграма и запустить все хендлеры
        await self.__client.run_until_disconnected()

    def run(self):
        """
        Запуск основного цикла asyncio.
        Стартуем таски клиента телеграма и шедулера
        """
        tasks = [self.__client.loop.create_task(self.start()),
                 self.__client.loop.create_task(self.__scheduler.run())]
        self.__client.loop.run_until_complete(asyncio.wait(tasks))
        self.__client.loop.close()

    def handleChatId(self, chat_id):
        """
        Проверяем ID чата на предмет 'не новый ли?'
         :param chat_id: ID чата
        """
        if chat_id not in self.__chats:
            self.__log.info("Found a new chat id %d", chat_id)
            self.addChat(chat_id)

    def addChat(self, chat_id):
        """
        Сохраняем ID чата, планируем задачи
        :param chat_id:
        :return:
        """
        if chat_id not in self.__chats:
            image_poster = ImagePoster(self, chat_id,
                                       config.GOOGLE_API_KEY,
                                       config.GOOGLE_SEARCH_ID)
            self.__scheduler.addTask(image_poster)
            self.__chats[chat_id] = ChatInfo(Head(self), image_poster)

    @events.register(events.NewMessage())
    async def message_handler(self, event: Message):
        """
        Обработка текстовых сообщений
        :param event:
        :return:
        """
        if config.TEST_MODE and event.chat_id not in config.TEST_MODE_CHAT_ID:
            return

        # Отдадим сообщение в голову
        self.handleChatId(event.chat_id)
        await self.__chats[event.chat_id].head.answer(event)

    async def send_message(self, *argc, **kwargs) -> Any:
        """
         Метод-прокси для отправки сообщений
        """
        try:
            return await self.client.send_message(*argc, **kwargs)
        except Exception as e:
            self.__log.exception(f"Error due send message: {e}")
            return None

    @property
    def name(self) -> str:
        return self.__me.username

    @property
    def id(self) -> Any:
        return self.__me.id

    @property
    def client(self) -> TelegramClient:
        return self.__client
