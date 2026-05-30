from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

router = Router()

CHANNEL_URL = "https://t.me/AstraStore09/73"


def catalog_channel_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📢 Открыть каталог в канале", url=CHANNEL_URL)],
        [InlineKeyboardButton(text="💬 Связаться с менеджером", callback_data="contact_manager")],
        [InlineKeyboardButton(text="◀️ Главное меню", callback_data="main_menu")],
    ])


@router.callback_query(F.data == "catalog_new")
async def show_catalog_new(callback: CallbackQuery):
    await callback.message.edit_text(
        "📱 <b>Новые устройства Apple</b>\n\n"
        "Актуальный каталог с ценами и фото — в нашем Telegram-канале.\n\n"
        "Нажмите кнопку ниже 👇",
        parse_mode="HTML",
        reply_markup=catalog_channel_keyboard()
    )


@router.callback_query(F.data == "catalog_used")
async def show_catalog_used(callback: CallbackQuery):
    await callback.message.edit_text(
        "♻️ <b>Устройства Apple б/у</b>\n\n"
        "Актуальный каталог с ценами и фото — в нашем Telegram-канале.\n\n"
        "Нажмите кнопку ниже 👇",
        parse_mode="HTML",
        reply_markup=catalog_channel_keyboard()
    )
