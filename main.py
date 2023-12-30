import asyncio

from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode

from aiogram.fsm.storage.memory import MemoryStorage
from router import router


asy def token
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    asyncio.run(main())
