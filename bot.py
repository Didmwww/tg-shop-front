import asyncio
import json
import logging
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "8597216818:AAF8SKNftoMB_ykPlK4n7LvtqM7mmtobl0o"
WEB_APP_URL = "https://didmwww.github.io/tg-shop-front/"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()

PRODUCTS = {
    "1": {"name": "iPhone 15 Pro", "price": 42000},
    "2": {"name": "MacBook Air", "price": 54000},
    "3": {"name": "Худі Oversize", "price": 1200},
    "4": {"name": "Кепка NY", "price": 600},
    "5": {"name": "Піца Pepperoni", "price": 350},
    "6": {"name": "AirPods Pro", "price": 9000},
}

web_app_btn = KeyboardButton(text="📱 Відкрити TechStore", web_app=WebAppInfo(url=WEB_APP_URL))
keyboard = ReplyKeyboardMarkup(keyboard=[[web_app_btn]], resize_keyboard=True)

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer(
        "👋 Вітаю в *TechStore*!\nНатисни кнопку нижче, щоб відкрити каталог.",
        parse_mode="Markdown",
        reply_markup=keyboard
    )

@dp.message(F.web_app_data)
async def web_app_data_handler(message: types.Message):
    data = json.loads(message.web_app_data.data)
    
    total_price = 0
    items_text = ""

    for item_id, quantity in data.items():
        if quantity > 0 and item_id in PRODUCTS:
            product = PRODUCTS[item_id]
            cost = product['price'] * quantity
            total_price += cost
            items_text += f"▫️ {product['name']} x{quantity} — *{cost} ₴*\n"

    if total_price == 0:
        return await message.answer("Кошик порожній 😢")

    text = (
        f"✅ *Нове замовлення!*\n\n"
        f"{items_text}\n"
        f"💳 *До сплати: {total_price} ₴*\n\n"
        f"Менеджер зв'яжеться з вами для підтвердження."
    )

    pay_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"💳 Оплатити {total_price} ₴", callback_data="pay_dummy")]
    ])
    
    await message.answer(text, parse_mode="Markdown", reply_markup=pay_kb)


@dp.callback_query(F.data == "pay_dummy")
async def pay_handler(callback: types.CallbackQuery):
    await callback.answer("Це демо-оплата. Гроші не списано!", show_alert=True)

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())