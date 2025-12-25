from aiogram import Bot, Dispatcher, types
from aiogram.enums import ChatMemberStatus
from aiogram.filters import Command

from config import CHANNEL_ID  # Импортируем общий канал


def create_bot(token: str, bot_name: str = "Бот"):
    """Создает и настраивает экземпляр бота с общей логикой."""
    bot = Bot(token=token)
    dp = Dispatcher()

    # ОБЩАЯ ФУНКЦИЯ ПРОВЕРКИ ПОДПИСКИ
    async def check_sub(user_id: int) -> bool:
        try:
            member = await bot.get_chat_member(CHANNEL_ID, user_id)
            return member.status in [
                ChatMemberStatus.CREATOR,
                ChatMemberStatus.ADMINISTRATOR,
                ChatMemberStatus.MEMBER,
            ]
        except Exception:
            return False

    # ОБЩАЯ КОМАНДА /start
    @dp.message(Command("start"))
    async def cmd_start(message: types.Message):
        if await check_sub(message.from_user.id):
            await message.answer(f"✅ Вы подписаны! Добро пожаловать в {bot_name}.")
        else:
            kb = types.InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        types.InlineKeyboardButton(
                            text="📢 Подписаться на канал",
                            url=f"https://t.me/{CHANNEL_ID.lstrip('@')}",
                        )
                    ],
                    [types.InlineKeyboardButton(text="✅ Я подписался", callback_data="check")],
                ]
            )
            await message.answer(
                f"Для работы с {bot_name} подпишитесь на канал: {CHANNEL_ID}", reply_markup=kb
            )

    # ОБЩАЯ ПРОВЕРКА ПО КНОПКЕ
    @dp.callback_query(lambda c: c.data == "check")
    async def callback_check(callback: types.CallbackQuery):
        if await check_sub(callback.from_user.id):
            await callback.message.edit_text(f"✅ Отлично! {bot_name} готов к работе.")
        else:
            await callback.answer("❌ Вы всё ещё не подписаны.", show_alert=True)

    return bot, dp, bot_name
