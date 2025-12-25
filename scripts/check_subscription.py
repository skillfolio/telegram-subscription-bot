import asyncio
import os
import sys

from aiogram import Bot
from aiogram.enums import ChatMemberStatus

from config import CHANNEL_ID


async def main() -> int:
    bot_token = os.getenv("BOT_TOKEN")
    user_id_raw = os.getenv("USER_ID")
    channel_id = os.getenv("CHANNEL_ID", CHANNEL_ID)

    if not bot_token:
        print("❌ BOT_TOKEN is not set.")
        return 2
    if not user_id_raw:
        print("❌ USER_ID is not set.")
        return 2

    try:
        user_id = int(user_id_raw)
    except ValueError:
        print("❌ USER_ID must be an integer.")
        return 2

    bot = Bot(token=bot_token)
    try:
        member = await bot.get_chat_member(channel_id, user_id)
        subscribed = member.status in {
            ChatMemberStatus.CREATOR,
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.MEMBER,
        }
        if subscribed:
            print("✅ subscribed")
            return 0
        print("❌ not subscribed")
        return 1
    except Exception as exc:
        print(f"❌ failed to check subscription: {exc}")
        return 3
    finally:
        await bot.session.close()


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
