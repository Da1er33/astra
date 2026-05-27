from aiogram import Router, F, Bot
from aiogram.types import (
    CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton
)
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from config import MANAGER_CHAT_ID

router = Router()


class TradeInForm(StatesGroup):
    device = State()
    model = State()
    condition = State()
    name = State()
    phone = State()


CONDITIONS = {
    "perfect": "⭐️ Идеальное — без царапин и следов использования",
    "good": "👍 Хорошее — мелкие царапины, всё работает",
    "fair": "😐 Среднее — видимые повреждения, всё работает",
    "bad": "⚠️ Плохое — трещины / не работают функции",
}

TRADEIN_DEVICES = ["iPhone", "iPad", "MacBook", "Apple Watch", "AirPods", "Другое"]


def tradein_devices_keyboard() -> InlineKeyboardMarkup:
    buttons = [[InlineKeyboardButton(text=d, callback_data=f"ti_dev_{i}")]
               for i, d in enumerate(TRADEIN_DEVICES)]
    buttons.append([InlineKeyboardButton(text="◀️ Главное меню", callback_data="main_menu")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def conditions_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text=label, callback_data=f"ti_cond_{key}")]
        for key, label in CONDITIONS.items()
    ]
    buttons.append([InlineKeyboardButton(text="❌ Отмена", callback_data="main_menu")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def cancel_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="❌ Отмена", callback_data="main_menu")]
    ])


@router.callback_query(F.data == "tradein")
async def tradein_start(callback: CallbackQuery, state: FSMContext):
    await state.set_state(TradeInForm.device)
    await callback.message.edit_text(
        "🔄 <b>Trade-In — оценка устройства</b>\n\n"
        "Сдайте старое устройство и получите скидку на новое!\n\n"
        "Какое устройство хотите сдать?",
        parse_mode="HTML",
        reply_markup=tradein_devices_keyboard()
    )


@router.callback_query(F.data.startswith("ti_dev_"), TradeInForm.device)
async def tradein_device(callback: CallbackQuery, state: FSMContext):
    index = int(callback.data.split("_")[2])
    device = TRADEIN_DEVICES[index]
    await state.update_data(device=device)
    await state.set_state(TradeInForm.model)
    await callback.message.edit_text(
        f"✅ Устройство: <b>{device}</b>\n\n"
        f"📝 Укажите модель и объём памяти\n"
        f"<i>Например: iPhone 13 128GB или MacBook Air M1 8/256</i>",
        parse_mode="HTML",
        reply_markup=cancel_keyboard()
    )


@router.message(TradeInForm.model)
async def tradein_model(message: Message, state: FSMContext):
    await state.update_data(model=message.text)
    await state.set_state(TradeInForm.condition)
    await message.answer(
        "🔍 Оцените состояние устройства:",
        reply_markup=conditions_keyboard()
    )


@router.callback_query(F.data.startswith("ti_cond_"), TradeInForm.condition)
async def tradein_condition(callback: CallbackQuery, state: FSMContext):
    cond_key = callback.data.replace("ti_cond_", "")
    cond_label = CONDITIONS[cond_key]
    await state.update_data(condition=cond_label)
    await state.set_state(TradeInForm.name)
    await callback.message.edit_text(
        f"✅ Состояние: <b>{cond_label}</b>\n\n👤 Как вас зовут?",
        parse_mode="HTML",
        reply_markup=cancel_keyboard()
    )


@router.message(TradeInForm.name)
async def tradein_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(TradeInForm.phone)
    await message.answer("📞 Введите ваш номер телефона:", reply_markup=cancel_keyboard())


@router.message(TradeInForm.phone)
async def tradein_phone(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    await state.clear()

    user = message.from_user
    username = f"@{user.username}" if user.username else "нет username"

    # Уведомление менеджеру
    manager_text = (
        f"🔄 <b>НОВАЯ ЗАЯВКА TRADE-IN</b>\n\n"
        f"👤 Имя: {data['name']}\n"
        f"📞 Телефон: {message.text}\n"
        f"📱 Устройство: {data['device']}\n"
        f"📋 Модель: {data['model']}\n"
        f"🔍 Состояние: {data['condition']}\n\n"
        f"💬 Telegram: {username}\n"
        f"🆔 User ID: {user.id}"
    )
    await bot.send_message(MANAGER_CHAT_ID, manager_text, parse_mode="HTML")

    from keyboards.main_menu import back_to_menu_keyboard
    await message.answer(
        f"✅ <b>Заявка на Trade-In принята!</b>\n\n"
        f"Наш менеджер оценит ваше устройство и свяжется с вами по номеру <b>{message.text}</b>.\n\n"
        f"Как правило, это занимает не более 30 минут в рабочее время. 🍎",
        parse_mode="HTML",
        reply_markup=back_to_menu_keyboard()
    )
