import asyncio
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN
from handlers import catalog, repair, tradein, manager_contact, promo_faq
from keyboards.main_menu import main_menu_keyboard

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# Подключаем роутеры
dp.include_router(catalog.router)
dp.include_router(repair.router)
dp.include_router(tradein.router)
dp.include_router(manager_contact.router)
dp.include_router(promo_faq.router)


@dp.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        f"👋 Добро пожаловать в <b>Астра Сторе</b>!\n\n"
        f"Мы занимаемся продажей новой и б/у техники Apple, "
        f"ремонтом устройств и Trade-In.\n\n"
        f"Выберите, что вас интересует:",
        parse_mode="HTML",
        reply_markup=main_menu_keyboard()
    )


@dp.callback_query(F.data == "main_menu")
async def back_to_main(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text(
        "🏠 <b>Главное меню</b>\n\nВыберите, что вас интересует:",
        parse_mode="HTML",
        reply_markup=main_menu_keyboard()
    )


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
