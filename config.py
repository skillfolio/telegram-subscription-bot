import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any


DEFAULT_CONFIG_PATH = "bot_settings.json"


@dataclass(frozen=True)
class BotDefinition:
    name: str
    token_env: str


@dataclass(frozen=True)
class Messages:
    success: str
    subscribe_prompt: str
    not_subscribed_alert: str
    subscribe_button: str
    check_button: str


@dataclass(frozen=True)
class AppConfig:
    channel_id: int
    channel_invite_link: str
    bots: list[BotDefinition]
    messages: Messages


def _read_json_config(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}

    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    if not isinstance(data, dict):
        raise ValueError("Config root must be a JSON object.")

    return data


def _build_bots(raw_bots: Any) -> list[BotDefinition]:
    if not raw_bots:
        return []

    bots: list[BotDefinition] = []
    for index, raw_bot in enumerate(raw_bots, start=1):
        if not isinstance(raw_bot, dict):
            raise ValueError(f"Bot definition #{index} must be an object.")

        name = str(raw_bot.get("name", "")).strip()
        token_env = str(raw_bot.get("token_env", "")).strip()

        if not name or not token_env:
            raise ValueError(
                f"Bot definition #{index} must contain non-empty 'name' and 'token_env'."
            )

        bots.append(BotDefinition(name=name, token_env=token_env))

    return bots


def load_app_config() -> AppConfig:
    config_path = Path(os.getenv("BOT_CONFIG_FILE", DEFAULT_CONFIG_PATH))
    raw = _read_json_config(config_path)

    channel = raw.get("channel", {})
    messages = raw.get("messages", {})

    channel_id = int(os.getenv("CHANNEL_ID", channel.get("id", -1002634329403)))
    channel_invite_link = os.getenv(
        "CHANNEL_INVITE_LINK", channel.get("invite_link", "https://t.me/+6X0TJ_GZcp5jZTMy")
    )

    configured_bots = _build_bots(raw.get("bots", []))

    # Backward compatibility: previous mode with BOT_INSTANCE_NAME=<ENV_VAR_WITH_TOKEN>
    if not configured_bots:
        default_token_env = os.getenv("BOT_INSTANCE_NAME", "BOT_TOKEN")
        configured_bots = [BotDefinition(name=default_token_env, token_env=default_token_env)]

    loaded_messages = Messages(
        success=str(messages.get("success", "✅ Отлично! {bot_name} готов к работе.")),
        subscribe_prompt=str(
            messages.get(
                "subscribe_prompt",
                "Для работы с {bot_name} подпишитесь на канал и нажмите «Проверить подписку».",
            )
        ),
        not_subscribed_alert=str(messages.get("not_subscribed_alert", "❌ Вы всё ещё не подписаны.")),
        subscribe_button=str(messages.get("subscribe_button", "📣 Подписаться на канал")),
        check_button=str(messages.get("check_button", "✅ Проверить подписку")),
    )

    return AppConfig(
        channel_id=channel_id,
        channel_invite_link=channel_invite_link,
        bots=configured_bots,
        messages=loaded_messages,
    )
