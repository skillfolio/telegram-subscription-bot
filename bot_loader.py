import asyncio
import contextlib
import os
import sys

from bot_core import create_bot
from config import BotDefinition, load_app_config


async def _run_single_bot(bot_definition: BotDefinition, app_config):
    bot_token = os.getenv(bot_definition.token_env)
    if not bot_token:
        print(
            f"⚠️ Пропуск бота '{bot_definition.name}': "
            f"переменная окружения '{bot_definition.token_env}' не найдена."
        )
        return

    bot, dp, _ = create_bot(
        token=bot_token,
        bot_name=bot_definition.name,
        channel_id=app_config.channel_id,
        channel_invite_link=app_config.channel_invite_link,
        messages=app_config.messages,
    )

    await bot.delete_webhook(drop_pending_updates=True)
    print(f"🚀 Запускается бот: {bot_definition.name}")

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


async def run_bots():
    app_config = load_app_config()

    tasks = [asyncio.create_task(_run_single_bot(bot_definition, app_config)) for bot_definition in app_config.bots]

    if not tasks:
        print("❌ Не найдено ни одного бота в конфигурации.")
        sys.exit(1)

    if all(os.getenv(bot.token_env) is None for bot in app_config.bots):
        print("❌ Ни для одного бота не найден токен в переменных окружения.")
        sys.exit(1)

    try:
        await asyncio.gather(*tasks)
    except asyncio.CancelledError:
        pass
    finally:
        for task in tasks:
            task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await task


if __name__ == "__main__":
    asyncio.run(run_bots())
