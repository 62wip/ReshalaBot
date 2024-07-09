from functools import partial

import asyncio
from aiogram import Bot, Dispatcher

# Импортируем настройки и модули для клавиатур и обработчиков
# import app.keyboards as kb
from app.handlers import router as router
from config import *

async def on_startup(dp: Dispatcher) -> None:
    print("Bot is starting up...")

async def on_shutdown(dp: Dispatcher) -> None:
    print("Bot is shutting down...")
    
async def main() -> None:
    bot = Bot(token=API_TOKEN)
    await bot.delete_webhook(drop_pending_updates=True) 
    dp = Dispatcher()
    dp.include_router(router)
    dp.startup.register(partial(on_startup, dp))
    dp.shutdown.register(partial(on_shutdown, dp))
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt or RuntimeError:
        print('Exit successful.')
