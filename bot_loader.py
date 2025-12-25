import asyncio
import os
import sys

from bot_core import create_bot


async def run_bot():
    
    """Запускает одного бота. Его имя и токен берутся из переменных окружения."""
    # Имя бота (например, NEWS_BOT) берём из переменной окружения BOT_INSTANCE_NAME
    bot_instance_name = os.getenv("BOT_INSTANCE_NAME", "DEFAULT_BOT")
    # Токен берём из переменной окружения с тем же именем, что и BOT_INSTANCE_NAME
    bot_token = os.getenv(bot_instance_name)

if not bot_token:
        print(
            f"❌ Ошибка: Для экземпляра '{bot_instance_name}' не найден токен в переменной окружения."
        )
        sys.exit(1)

  bot, dp, bot_name = create_bot(token=bot_token, bot_name=bot_instance_name)
    print(f"🚀 Запускается бот: {bot_name} (экземпляр: {bot_instance_name})")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(run_bot())
