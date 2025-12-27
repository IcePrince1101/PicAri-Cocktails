import asyncio
import os
from pathlib import Path

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from logic import router

# 🔧 Загрузка переменных окружения
print(Path(__file__).resolve())
if os.path.exists(Path(__file__).resolve().parent / ".env"):
    load_dotenv(Path(__file__).resolve().parent / ".env")
    BOT_TOKEN = os.getenv("BOT_API_KEY")
else:
    print("🔴 Не удалось загрузить переменные окружения")
    exit(1)

async def main():
    # 📦 Инициализация глобальных объектов
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    try:
        dp.include_router(router)

        print("🤖 Бот запущен. Ожидаю события...")
        try:
            await dp.start_polling(bot, skip_updates=True)
        finally:
            await bot.session.close()

    except Exception as e:
        raise Exception(f"🔴 Во время запуска возникла ошибка: {e}")
    finally:
        print("🛑 Бот завершает работу. Закрываем соединения...")


if __name__ == "__main__":
    asyncio.run(main())