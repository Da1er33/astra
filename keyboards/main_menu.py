from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def main_menu_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(text="📱 Каталог новых", callback_data="catalog_new"),
            InlineKeyboardButton(text="♻️ Каталог б/у", callback_data="catalog_used"),
        ],
        [
            InlineKeyboardButton(text="🔥 Акции", callback_data="promo"),
        ],
        [
            InlineKeyboardButton(text="🔧 Записаться на ремонт", callback_data="repair"),
        ],
        [
            InlineKeyboardButton(text="🔄 Trade-In оценка", callback_data="tradein"),
        ],
        [
            InlineKeyboardButton(text="💬 Связь с менеджером", callback_data="contact_manager"),
        ],
        [
            InlineKeyboardButton(text="❓ Частые вопросы", callback_data="faq"),
        ],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def back_to_menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="◀️ Главное меню", callback_data="main_menu")]
    ])
