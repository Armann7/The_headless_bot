import asyncio
import logging
from collections import namedtuple

from app.task_manager.task import Task
from app import config

# Статусы шедулера
StatusSchedulerTuple = namedtuple("StatusScheduler", ["init", "running",
                                                      "stopping", "stopped"])
StatusScheduler = StatusSchedulerTuple(init=0, running=2,
                                       stopping=3, stopped=4)


class Scheduler:
    """
    Шедулер.
    Подход - каждые __time_slice секунд просыпаемся и проверяем, не пора ли стартовать какую-нибудь задачу
    """

    def __init__(self, time_slice=60):
        super().__init__()
        self.__time_slice = time_slice          # Время между тактами шедулера, сек
        self.__tasks = list()                   # Задачи
        self.__status = StatusScheduler.init    # Текущий статус шедулера
        self.__log = logging.getLogger(config.logUtils.gen_name(self))

    def addTask(self, task: Task):
        """
        Добавить задачу
        :param task:
        """
        self.__log.info(f"Task added: {task.name}")
        self.__tasks.append(task)

    async def run(self):
        """
        Запуск шедулера
        """
        if self.__status == StatusScheduler.stopped:
            return

        self.__status = StatusScheduler.running
        self.__log.info("Scheduler started")
        while True:
            # Если сигнал к остановке - тормозим
            if self.__status == StatusScheduler.stopping:
                break
            # Запускаем все задачи по очереди
            for task in self.__tasks:
                await task.execute()
            # Отдаем время другим
            await asyncio.sleep(self.__time_slice)
        self.__status = StatusScheduler.stopped
        self.__log.info("Scheduler stopped")

    async def stop(self):
        """
        Остановить шедулер
        """
        self.__status = StatusScheduler.stopping

    def hasActiveTasks(self) -> bool:
        """
        Есть ли активные задачи?
        :return:
        """
        for t in self.__tasks:
            if t.isActive:
                return True
        return False
