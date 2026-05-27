from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

router = Router()

# =============================================
# КАТАЛОГ ТОВАРОВ — редактируйте под свой ассортимент
# =============================================

CATALOG = {
    "new": [
        {
            "name": "iPhone 16 Pro Max 256GB",
            "price": "129 990 ₽",
            "desc": "Новый, запечатанный. Гарантия Apple 1 год.",
            "emoji": "📱"
        },
        {
            "name": "iPhone 16 128GB",
            "price": "89 990 ₽",
            "desc": "Новый, запечатанный. Все цвета в наличии.",
            "emoji": "📱"
        },
        {
            "name": "MacBook Air M3 13\" 8/256GB",
            "price": "119 990 ₽",
            "desc": "Новый, запечатанный. Гарантия Apple 1 год.",
            "emoji": "💻"
        },
        {
            "name": "AirPods Pro 2",
            "price": "24 990 ₽",
            "desc": "Новые, запечатанные.",
            "emoji": "🎧"
        },
        {
            "name": "Apple Watch Series 10 GPS 42mm",
            "price": "39 990 ₽",
            "desc": "Новые, запечатанные.",
            "emoji": "⌚"
        },
    ],
    "used": [
        {
            "name": "iPhone 15 Pro 256GB",
            "price": "74 990 ₽",
            "desc": "Состояние: отличное. АКБ 94%. Комплект полный.",
            "emoji": "📱"
        },
        {
            "name": "iPhone 14 128GB",
            "price": "54 990 ₽",
            "desc": "Состояние: хорошее. АКБ 89%. Без царапин.",
            "emoji": "📱"
        },
        {
            "name": "MacBook Pro M1 13\" 8/256GB",
            "price": "84 990 ₽",
            "desc": "Состояние: хорошее. Цикл заряда: 120.",
            "emoji": "💻"
        },
        {
            "name": "iPad Air 5 64GB Wi-Fi",
            "price": "44 990 ₽",
            "desc": "Состояние: отличное. АКБ 97%.",
            "emoji": "📟"
        },
    ]
}


def catalog_keyboard(items: list, category: str) -> InlineKeyboardMarkup:
    buttons = []
    for i, item in enumerate(items):
        buttons.append([
            InlineKeyboardButton(
                text=f"{item['emoji']} {item['name']} — {item['price']}",
                callback_data=f"item_{category}_{i}"
            )
        ])
    buttons.append([InlineKeyboardButton(text="◀️ Главное меню", callback_data="main_menu")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def item_detail_keyboard(category: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💬 Хочу купить — связаться", callback_data="contact_manager")],
        [InlineKeyboardButton(text="◀️ Назад к каталогу", callback_data=f"catalog_{category}")],
    ])


@router.callback_query(F.data == "catalog_new")
async def show_catalog_new(callback: CallbackQuery):
    items = CATALOG["new"]
    await callback.message.edit_text(
        "📱 <b>Новые устройства Apple</b>\n\nВыберите товар для подробной информации:",
        parse_mode="HTML",
        reply_markup=catalog_keyboard(items, "new")
    )


@router.callback_query(F.data == "catalog_used")
async def show_catalog_used(callback: CallbackQuery):
    items = CATALOG["used"]
    await callback.message.edit_text(
        "♻️ <b>Устройства Apple б/у</b>\n\nВыберите товар для подробной информации:",
        parse_mode="HTML",
        reply_markup=catalog_keyboard(items, "used")
    )


@router.callback_query(F.data.startswith("item_"))
async def show_item(callback: CallbackQuery):
    parts = callback.data.split("_")
    category = parts[1]
    index = int(parts[2])
    item = CATALOG[category][index]

    cat_label = "Новый" if category == "new" else "Б/у"

    text = (
        f"{item['emoji']} <b>{item['name']}</b>\n\n"
        f"💰 <b>Цена:</b> {item['price']}\n"
        f"📋 <b>Описание:</b> {item['desc']}\n"
        f"🏷 <b>Категория:</b> {cat_label}\n\n"
        f"Заинтересовал товар? Нажмите кнопку ниже — менеджер ответит вам в ближайшее время!"
    )

    await callback.message.edit_text(
        text,
        parse_mode="HTML",
        reply_markup=item_detail_keyboard(category)
    )
