import asyncio

from aiogram import Dispatcher
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import Message
from aiogram.utils.exceptions import Throttled


class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, limit: int = 0.7):
        BaseMiddleware.__init__(self)
        self.rate_limit = limit

    async def on_process_message(self, message: Message, data: dict):
        # handler = current_handler.get()
        dp = Dispatcher.get_current()

        # built-in anti-flood check
        try:
            await dp.throttle(key="antiflood_message", rate=self.rate_limit)  # sends a request with the name "key"
        except Throttled as _t:  # catches a request named "key"
            await self.msg_throttle(message, _t)

            raise CancelHandler()

    async def msg_throttle(self, message: Message, throttled: Throttled):
        delta = throttled.rate - throttled.delta

        if throttled.exceeded_count <= 2:
            await message.reply("Охлади свое траханье и не флуди 😡")

        await asyncio.sleep(delta)
