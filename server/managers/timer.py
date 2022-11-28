import asyncio


class Timer:
    def __init__(self, timeout, overtime_callback):
        print("CREATED A TIMER")
        self._timeout = timeout
        self._callback = overtime_callback
        self._task = asyncio.create_task(self._job())

    async def _job(self):
        print("JOB CALLED")
        await asyncio.sleep(self._timeout)
        print("TIME ENDED")
        await self._callback()

    def stop(self):
        self._task.cancel()


# async def players_timers(players, callback):
#     player.game_id: Timer(15, callback)
