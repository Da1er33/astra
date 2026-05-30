from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

router = Router()

# =============================================
# АКЦИИ — редактируйте под актуальные предложения
# =============================================

PROMOS = [
    {
        "emoji": "🔥",
        "title": "Trade-In + скидка 5 000 ₽",
        "desc": "Сдайте любой iPhone и получите скидку 5 000 ₽ на новый iPhone 16. Только до конца месяца.",
    },
    {
        "emoji": "🎁",
        "title": "Чехол в подарок",
        "desc": "При покупке любого iPhone б/у — чехол и защитное стекло в подарок.",
    },
    {
        "emoji": "🔧",
        "title": "Диагностика бесплатно",
        "desc": "Бесплатная диагностика любого устройства Apple. Без записи, в день обращения.",
    },
]

# =============================================
# FAQ — редактируйте под свои ответы
# =============================================

FAQ = [
    {
        "q": "Какая гарантия на б/у технику?",
        "a": "На все б/у устройства мы даём гарантию 30 дней. На новые — официальная гарантия Apple 1 год.",
    },
    {
        "q": "Как проходит ремонт?",
        "a": "Вы оставляете заявку → мастер диагностирует устройство бесплатно → согласовываем стоимость → делаем ремонт. Большинство ремонтов — в день обращения.",
    },
    {
        "q": "Можно ли купить в рассрочку?",
        "a": "Да, оформляем рассрочку 0% через партнёров. Уточните у менеджера актуальные условия.",
    },
    {
        "q": "Как проверить устройство перед покупкой?",
        "a": "Вы можете проверить любое устройство при встрече. Мы не торопим — проверяйте столько, сколько нужно.",
    },
    {
        "q": "Как узнать стоимость Trade-In?",
        "a": "Оставьте заявку через бота или напишите менеджеру. Оценку делаем в течение 30 минут в рабочее время.",
    },
]


def promo_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔄 Trade-In оценка", callback_data="tradein")],
        [InlineKeyboardButton(text="💬 Связаться с менеджером", callback_data="contact_manager")],
        [InlineKeyboardButton(text="◀️ Главное меню", callback_data="main_menu")],
    ])


def faq_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text=f"❓ {item['q']}", callback_data=f"faq_{i}")]
        for i, item in enumerate(FAQ)
    ]
    buttons.append([InlineKeyboardButton(text="◀️ Главное меню", callback_data="main_menu")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def faq_back_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="◀️ Назад к вопросам", callback_data="faq")],
        [InlineKeyboardButton(text="💬 Спросить менеджера", callback_data="contact_manager")],
    ])


@router.callback_query(F.data == "promo")
async def show_promo(callback: CallbackQuery):
    text = "🔥 <b>Акции и спецпредложения</b>\n\n"
    for p in PROMOS:
        text += f"{p['emoji']} <b>{p['title']}</b>\n{p['desc']}\n\n"
    text += "📞 Чтобы воспользоваться акцией — свяжитесь с менеджером или оставьте заявку на Trade-In."
    await callback.message.edit_text(text, parse_mode="HTML", reply_markup=promo_keyboard())


@router.callback_query(F.data == "faq")
async def show_faq(callback: CallbackQuery):
    await callback.message.edit_text(
        "❓ <b>Часто задаваемые вопросы</b>\n\nВыберите вопрос:",
        parse_mode="HTML",
        reply_markup=faq_keyboard()
    )


@router.callback_query(F.data.startswith("faq_"))
async def show_faq_answer(callback: CallbackQuery):
    index = int(callback.data.split("_")[1])
    item = FAQ[index]
    text = (
        f"❓ <b>{item['q']}</b>\n\n"
        f"💡 {item['a']}"
    )
    await callback.message.edit_text(text, parse_mode="HTML", reply_markup=faq_back_keyboard())
