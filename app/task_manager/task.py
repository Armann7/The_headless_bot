import logging
from typing import Optional
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from collections import namedtuple

from app import config


# Статусы задач
StatusTaskTuple = namedtuple("StatusTaskTuple", ["init", "waited",
                                                 "running", "stopped"])
StatusTask = StatusTaskTuple(init=0, waited=1, running=2, stopped=4)


class Task(ABC):
    """
    Задача для шедулера.
    Для переопределения предназначен абстрактный метод _do
    """
    def __init__(self, name: str):
        super().__init__()
        self.__name = name
        self._status = StatusTask.init
        self._log = logging.getLogger(config.logUtils.gen_name(self))

    async def execute(self):
        """
        Выполнение задачи
        :return:
        """
        if not self.isActive:
            return
        self.status = StatusTask.running
        self._logTaskRunning()
        await self._do()
        self.status = StatusTask.waited

    async def stop(self):
        self.status = StatusTask.stopped

    @property
    def isActive(self) -> bool:
        """ Задача в активном статусе? """
        if self.status == StatusTask.stopped:
            return False
        else:
            return True

    @property
    def name(self) -> str:
        return self.__name

    @property
    def status(self) -> int:
        return self._status

    @status.setter
    def status(self, status: int):
        if self.isActive:
            self._status = status

    def _logTaskRunning(self):
        self._log.info(f"{datetime.now():%H:%M:%S} - task '{self.name}' running")

    @abstractmethod
    async def _do(self):
        """
        Полезная нагрузка
        :return:
        """
        pass


class PlanningTask(Task, ABC):
    """
    Задача для шедулера, планируемая на определенное время.
    Для переопределения абстрактные методы _planNextRun и _do
    """
    def __init__(self, name: str, plan_time: datetime = None, tolerance=config.TASK_PLAN_TIME_TOLERANCE):
        super().__init__(name)
        self.__tolerance_time = timedelta(seconds=tolerance)    # Допустимое время отклонения срока запуска (сек)
        self.__planTime = plan_time                             # Плановые дата и время запуска
        self._log = logging.getLogger(config.logUtils.gen_name(self))

    @property
    def planTime(self) -> Optional[datetime]:
        return self.__planTime

    @planTime.setter
    def planTime(self, plan_time):
        self.__planTime = plan_time

    def _isTimeToRun(self) -> bool:
        """
        Пора запускаться?
        :return:
        """
        if not self.planTime:
            return False
        dt_current = datetime.now()
        if dt_current < self.planTime:
            # Время еще не настало
            return False
        else:
            # Время запуска прошло. Проверяем, в допустимых ли пределах
            max_start_time = self.planTime + self.__tolerance_time    # Максимально допустимое время запуска
            if dt_current <= max_start_time:
                self._log.info(f"Task {self.name}, time to run ({dt_current})")
                return True
            else:
                raise TaskExecutionSkipped(self.name, self.planTime)

    @abstractmethod
    def _planNextRun(self):
        """
        Планируем следующее время запуска.
        :return:
        """
        pass

    @abstractmethod
    async def _do(self):
        """
        Полезная нагрузка
        :return:
        """
        pass

    async def execute(self):
        if not self.isActive:
            return
        try:
            if self._isTimeToRun():
                self._logTaskRunning()
                await self._do()
                self._planNextRun()
        except TaskExecutionSkipped as e:
            self._log.error(f"{e}")
            self._planNextRun()


class TaskExecutionSkipped(Exception):
    """
    Исключение - пропущено время старта задачи
    """
    def __init__(self, *args):
        self.name = None
        self.plan_time = None
        if args:
            self.name = args[0]
            self.plan_time = args[1]

    def __str__(self) -> str:
        if self.name:
            return f'Пропущено время выполнения задачи {self.name} (плановое время {self.plan_time:%H:%M:%S})'
        return 'Пропущено время выполнения задачи'
