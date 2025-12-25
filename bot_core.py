from aiogram import Bot, Dispatcher, types
from aiogram.enums import ChatMemberStatus
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import CHANNEL_ID, CHANNEL_INVITE_LINK


def create_bot(token: str, bot_name: str = "Бот"):
    bot = Bot(token=token)
    dp = Dispatcher()

    async def is_subscribed(user_id: int) -> bool:
        try:
            member = await bot.get_chat_member(CHANNEL_ID, user_id)
            return member.status in {
                ChatMemberStatus.MEMBER,
                ChatMemberStatus.ADMINISTRATOR,
                ChatMemberStatus.CREATOR,
            }
        except Exception:
            # Если бот не админ канала / неверный ID / нет доступа — вернем False
            return False

    def subscribe_keyboard():
        kb = InlineKeyboardBuilder()
        kb.button(text="📣 Подписаться на канал", url=CHANNEL_INVITE_LINK)
        kb.button(text="✅ Проверить подписку", callback_data="check_sub")
        kb.adjust(1)
        return kb.as_markup()

    @dp.message(Command("start"))
    async def cmd_start(message: types.Message):
        if await is_subscribed(message.from_user.id):
            await message.answer(f"✅ Отлично! {bot_name} готов к работе.")
        else:
            await message.answer(
                f"Для работы с {bot_name} подпишитесь на канал и нажмите «Проверить подписку».",
                reply_markup=subscribe_keyboard(),
            )

    @dp.callback_query(lambda c: c.data == "check_sub")
    async def callback_check(callback: types.CallbackQuery):
        if await is_subscribed(callback.from_user.id):
            await callback.message.edit_text(f"✅ Отлично! {bot_name} готов к работе.")
        else:
            await callback.answer("❌ Вы всё ещё не подписаны.", show_alert=True)

    return bot, dp, bot_name
