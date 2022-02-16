import pytest
import asyncio
from app.task_manager.scheduler import Scheduler
from app.task_manager.task import Task, PlanningTask
from datetime import datetime, timedelta


counter_task = 0
counter_planTask = 0

counter_task_value = 5
counter_planTask_value = 2


@pytest.mark.app_scheduler
def test_scheduler():
    global counter_task, counter_planTask
    counter_task = counter_planTask = 0

    runAsync()
    assert counter_task == counter_task_value
    assert counter_planTask == counter_planTask_value


class TaskSimple(Task):
    async def _do(self):
        global counter_task
        counter_task += 1
        if counter_task == counter_task_value:
            await self.stop()


class TaskPlanning(PlanningTask):
    def __init__(self, name: str):
        super().__init__(name, tolerance=30)
        self._planNextRun()

    def _planNextRun(self):
        self.planTime = datetime.now() + timedelta(seconds=15)

    async def _do(self):
        global counter_planTask
        counter_planTask += 1
        if counter_planTask == counter_planTask_value:
            await self.stop()


async def stopScheduler(scheduler):
    while True:
        if not scheduler.hasActiveTasks():
            await scheduler.stop()
            break
        await asyncio.sleep(0)


def runAsync():
    scheduler = Scheduler(time_slice=2)
    scheduler.addTask(TaskSimple("Test task"))
    scheduler.addTask(TaskPlanning("Test plan task"))

    try:
        ioloop = asyncio.get_event_loop()
    except RuntimeError:
        ioloop = asyncio.new_event_loop()
    tasks = [ioloop.create_task(scheduler.run()), ioloop.create_task(stopScheduler(scheduler))]
    # asyncio.run(asyncio.wait(tasks))
    ioloop.run_until_complete(asyncio.wait(tasks))
    ioloop.close()


if __name__ == '__main__':
    pytest.main()
