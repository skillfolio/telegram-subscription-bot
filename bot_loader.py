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
    except Exception as e:
        print(f"❌ Ошибка в работе бота '{bot_definition.name}': {e}", file=sys.stderr)
    finally:
        await bot.session.close()


def _get_runnable_bots(bot_definitions: list[BotDefinition]) -> list[BotDefinition]:
    runnable: list[BotDefinition] = []
    seen_tokens: dict[str, str] = {}

    for bot_definition in bot_definitions:
        bot_token = os.getenv(bot_definition.token_env)
        if not bot_token:
            print(
                f"⚠️ Пропуск бота '{bot_definition.name}': "
                f"переменная окружения '{bot_definition.token_env}' не найдена."
            )
            continue

        duplicate_name = seen_tokens.get(bot_token)
        if duplicate_name:
            print(
                f"⚠️ Пропуск бота '{bot_definition.name}': токен совпадает с ботом "
                f"'{duplicate_name}'. Проверьте переменные окружения — одинаковые токены "
                f"вызывают TelegramConflictError."
            )
            continue

        seen_tokens[bot_token] = bot_definition.name
        runnable.append(bot_definition)

    return runnable


async def run_bots():
    app_config = load_app_config()

    runnable_bots = _get_runnable_bots(app_config.bots)

    if not app_config.bots:
        print("❌ Не найдено ни одного бота в конфигурации.")
        sys.exit(1)

    if not runnable_bots:
        print(
            "❌ Нет ботов для запуска: проверьте токены в переменных окружения и "
            "убедитесь, что токены не дублируются."
        )
        sys.exit(1)

    tasks = [asyncio.create_task(_run_single_bot(bot_definition, app_config)) for bot_definition in runnable_bots]

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
