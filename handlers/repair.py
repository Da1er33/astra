from aiogram import Router, F, Bot
from aiogram.types import (
    CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton
)
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from config import MANAGER_CHAT_ID

router = Router()


class RepairForm(StatesGroup):
    device = State()
    problem = State()
    name = State()
    phone = State()


DEVICES = ["iPhone", "iPad", "MacBook", "Apple Watch", "AirPods", "iMac / Mac mini", "Другое"]


def devices_keyboard() -> InlineKeyboardMarkup:
    buttons = [[InlineKeyboardButton(text=d, callback_data=f"repair_device_{i}")]
               for i, d in enumerate(DEVICES)]
    buttons.append([InlineKeyboardButton(text="◀️ Главное меню", callback_data="main_menu")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


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


@router.callback_query(F.data == "repair")
async def repair_start(callback: CallbackQuery, state: FSMContext):
    await state.set_state(RepairForm.device)
    await callback.message.edit_text(
        "🔧 <b>Запись на ремонт</b>\n\nКакое устройство нужно отремонтировать?",
        parse_mode="HTML",
        reply_markup=devices_keyboard()
    )


@router.callback_query(F.data.startswith("repair_device_"), RepairForm.device)
async def repair_device(callback: CallbackQuery, state: FSMContext):
    index = int(callback.data.split("_")[2])
    device = DEVICES[index]
    await state.update_data(device=device)
    await state.set_state(RepairForm.problem)
    await callback.message.edit_text(
        f"✅ Устройство: <b>{device}</b>\n\n"
        f"📝 Опишите неисправность (что сломалось, что не работает):",
        parse_mode="HTML",
        reply_markup=cancel_keyboard()
    )


@router.message(RepairForm.problem)
async def repair_problem(message: Message, state: FSMContext):
    await state.update_data(problem=message.text)
    await state.set_state(RepairForm.name)
    await message.answer("👤 Как вас зовут?", reply_markup=cancel_keyboard())


@router.message(RepairForm.name)
async def repair_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(RepairForm.phone)
    await message.answer("📞 Введите ваш номер телефона:", reply_markup=cancel_keyboard())


@router.message(RepairForm.phone)
async def repair_phone(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    await state.clear()

    user = message.from_user
    username = f"@{user.username}" if user.username else "нет username"

    manager_text = (
        f"🔧 <b>НОВАЯ ЗАЯВКА НА РЕМОНТ</b>\n\n"
        f"👤 Имя: {data['name']}\n"
        f"📞 Телефон: {message.text}\n"
        f"📱 Устройство: {data['device']}\n"
        f"🛠 Проблема: {data['problem']}\n\n"
        f"💬 Telegram: {username}\n"
        f"🆔 User ID: {user.id}"
    )

    await bot.send_message(
        MANAGER_CHAT_ID,
        manager_text,
        parse_mode="HTML",
        reply_markup=manager_reply_keyboard(user.id, username)
    )

    from keyboards.main_menu import back_to_menu_keyboard
    await message.answer(
        f"✅ <b>Заявка принята!</b>\n\n"
        f"Наш менеджер свяжется с вами в ближайшее время по номеру <b>{message.text}</b>.\n\n"
        f"Спасибо, что выбрали Астра Сторе! 🍎",
        parse_mode="HTML",
        reply_markup=back_to_menu_keyboard()
    )
