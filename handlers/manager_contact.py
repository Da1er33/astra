from aiogram import Router, F, Bot
from aiogram.types import (
    CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton
)
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from config import MANAGER_CHAT_ID

router = Router()


class ContactForm(StatesGroup):
    question = State()


def cancel_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="❌ Отмена", callback_data="main_menu")]
    ])


def manager_reply_keyboard(user_id: int, username: str) -> InlineKeyboardMarkup:
    buttons = []
    if username and username != "нет username":
        buttons.append([
            InlineKeyboardButton(
                text="💬 Ответить клиенту",
                url=f"https://t.me/{username.lstrip('@')}"
            )
        ])
    else:
        buttons.append([
            InlineKeyboardButton(
                text="💬 Написать клиенту",
                url=f"tg://user?id={user_id}"
            )
        ])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


@router.callback_query(F.data == "contact_manager")
async def contact_start(callback: CallbackQuery, state: FSMContext):
    await state.set_state(ContactForm.question)
    await callback.message.edit_text(
        "💬 <b>Связь с менеджером</b>\n\n"
        "Напишите ваш вопрос или оставьте номер телефона — менеджер ответит вам в Telegram или перезвонит.\n\n"
        "<i>📍 Санкт-Петербург, 1-ая Советская, 10\n"
        "🕐 Пн–Вс с 12:00 до 20:00</i>",
        parse_mode="HTML",
        reply_markup=cancel_keyboard()
    )


@router.message(ContactForm.question)
async def contact_send(message: Message, state: FSMContext, bot: Bot):
    await state.clear()
    user = message.from_user
    username = f"@{user.username}" if user.username else "нет username"
    full_name = user.full_name

    manager_text = (
        f"💬 <b>ВОПРОС ОТ КЛИЕНТА</b>\n\n"
        f"👤 Имя: {full_name}\n"
        f"🔗 Telegram: {username}\n"
        f"🆔 User ID: <code>{user.id}</code>\n\n"
        f"📩 Сообщение:\n{message.text}"
    )

    await bot.send_message(
        MANAGER_CHAT_ID,
        manager_text,
        parse_mode="HTML",
        reply_markup=manager_reply_keyboard(user.id, username)
    )

    from keyboards.main_menu import back_to_menu_keyboard
    await message.answer(
        "✅ <b>Сообщение отправлено!</b>\n\n"
        "Менеджер свяжется с вами в ближайшее время.\n\n"
        "📍 Санкт-Петербург, 1-ая Советская, 10\n"
        "🕐 Пн–Вс с 12:00 до 20:00 🍎",
        parse_mode="HTML",
        reply_markup=back_to_menu_keyboard()
    )
