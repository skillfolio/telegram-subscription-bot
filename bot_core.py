from aiogram import Bot, Dispatcher, types
from aiogram.enums import ChatMemberStatus
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import Messages


def create_bot(
    *,
    token: str,
    bot_name: str,
    channel_id: int,
    channel_invite_link: str,
    messages: Messages,
):
    bot = Bot(token=token)
    dp = Dispatcher()

    async def is_subscribed(user_id: int) -> bool:
        try:
            member = await bot.get_chat_member(channel_id, user_id)
            return member.status in {
                ChatMemberStatus.MEMBER,
                ChatMemberStatus.ADMINISTRATOR,
                ChatMemberStatus.CREATOR,
            }
        except Exception:
            return False

    def subscribe_keyboard():
        kb = InlineKeyboardBuilder()
        kb.button(text=messages.subscribe_button, url=channel_invite_link)
        kb.button(text=messages.check_button, callback_data="check_sub")
        kb.adjust(1)
        return kb.as_markup()

    @dp.message(Command("start"))
    async def cmd_start(message: types.Message):
        if await is_subscribed(message.from_user.id):
            await message.answer(messages.success.format(bot_name=bot_name))
        else:
            await message.answer(
                messages.subscribe_prompt.format(bot_name=bot_name),
                reply_markup=subscribe_keyboard(),
            )

    @dp.callback_query(lambda c: c.data == "check_sub")
    async def callback_check(callback: types.CallbackQuery):
        if await is_subscribed(callback.from_user.id):
            await callback.message.edit_text(messages.success.format(bot_name=bot_name))
        else:
            await callback.answer(messages.not_subscribed_alert, show_alert=True)

    return bot, dp, bot_name
