import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.storage.memory import MemoryStorage

# ===== НАСТРОЙКИ =====
API_TOKEN = "8977388953:AAHotGE-Tot2hr51tBU1PwbjsEDPpMCdvPY"
YOUR_TELEGRAM_ID = 8399721205
CARD_NUMBER = "2204 3211 6696 1912"
# ====================

bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=MemoryStorage())
logging.basicConfig(level=logging.INFO)

PRODUCTS = {
    "marijuana_0.5": {"name": "🌿 Марихуана 0.5г", "price": 375},
    "marijuana_2": {"name": "🌿 Марихуана 2г", "price": 1250},
    "marijuana_5": {"name": "🌿 Марихуана 5г", "price": 2850},
    "cocaine_0.5": {"name": "❄️ Кокаин 0.5г", "price": 3400},
    "cocaine_2": {"name": "❄️ Кокаин 2г", "price": 11250},
    "cocaine_5": {"name": "❄️ Кокаин 5г", "price": 27000},
    "mephedrone_0.5": {"name": "💊 Мефедрон 0.5г", "price": 1200},
    "mephedrone_2": {"name": "💊 Мефедрон 2г", "price": 3650},
    "mephedrone_5": {"name": "💊 Мефедрон 5г", "price": 8000},
    "ketamine_0.5": {"name": "🐴 Кетамин 0.5г", "price": 2100},
    "ketamine_2": {"name": "🐴 Кетамин 2г", "price": 6750},
    "ketamine_5": {"name": "🐴 Кетамин 5г", "price": 15000},
    "amphetamine_0.5": {"name": "⚡ Амфетамин 0.5г", "price": 700},
    "amphetamine_2": {"name": "⚡ Амфетамин 2г", "price": 2000},
    "amphetamine_5": {"name": "⚡ Амфетамин 5г", "price": 4250},
}

orders = {}

@dp.message(Command("start"))
async def start(message: types.Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📦 Каталог", callback_data="catalog")],
        [InlineKeyboardButton(text="❓ Поддержка", callback_data="support")]
    ])
    await message.answer(
        "🔌 Добро пожаловать.\n"
        "Выбери действие:",
        reply_markup=kb
    )

@dp.callback_query(lambda c: c.data == "support")
async def support(callback: types.CallbackQuery):
    await callback.message.answer(
        "Напиши свой вопрос одним сообщением.\n"
        "Я передам его продавцу."
    )
    await callback.answer()

@dp.message(lambda msg: msg.reply_to_message and "поддержк" in str(msg.reply_to_message.text).lower())
async def forward_support(message: types.Message):
    await bot.send_message(
        YOUR_TELEGRAM_ID,
        f"📩 Вопрос от @{message.from_user.username or 'no'} (ID: {message.from_user.id}):\n\n{message.text}"
    )
    await message.answer("✅ Вопрос отправлен продавцу. Ожидай ответа.")

@dp.callback_query(lambda c: c.data == "catalog")
async def catalog(callback: types.CallbackQuery):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"{p['name']} — {p['price']} ₽", callback_data=f"buy_{k}")]
        for k, p in PRODUCTS.items()
    ])
    await callback.message.answer("📋 Выбери товар:", reply_markup=kb)
    await callback.answer()

@dp.callback_query(lambda c: c.data.startswith("buy_"))
async def buy(callback: types.CallbackQuery):
    key = callback.data.replace("buy_", "")
    product = PRODUCTS.get(key)
    if not product:
        await callback.answer("Товар недоступен")
        return

    user_id = callback.from_user.id
    orders[user_id] = {"product": product, "paid": False}

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Я оплатил", callback_data="confirm")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="catalog")]
    ])

    await callback.message.answer(
        f"🧾 Товар: {product['name']}\n"
        f"💰 Сумма: {product['price']} ₽\n\n"
        f"💳 Переведи точную сумму на карту:\n"
        f"`{CARD_NUMBER}`\n\n"
        f"⚠️ После перевода нажми кнопку «Я оплатил».",
        reply_markup=kb,
        parse_mode="Markdown"
    )
    await callback.answer()

@dp.callback_query(lambda c: c.data == "confirm")
async def confirm(callback: types.CallbackQuery):
    user_id = callback.from_user.id

    if user_id not in orders:
        await callback.message.answer("❌ Заказ не найден. Начни сначала /start")
        await callback.answer()
        return

    if orders[user_id]["paid"]:
        await callback.message.answer("⏳ Этот заказ уже был оплачен.")
        await callback.answer()
        return

    order = orders[user_id]

    await bot.send_message(
        YOUR_TELEGRAM_ID,
        f"🔔 НОВАЯ ОПЛАТА\n"
        f"━━━━━━━━━━━━━━━━\n"
        f"👤 Юзернейм: @{callback.from_user.username or 'нет'}\n"
        f"🆔 ID: {user_id}\n"
        f"📦 Товар: {order['product']['name']}\n"
        f"💰 Сумма: {order['product']['price']} ₽\n"
        f"━━━━━━━━━━━━━━━━\n"
        f"✏️ Напиши этому человеку в Telegram сам."
    )

    orders[user_id]["paid"] = True

    await callback.message.answer(
        "✅ Оплата подтверждена.\n"
        "Свяжусь с тобой в ближайшее время."
    )
    await callback.answer()

@dp.message(lambda msg: msg.text and not msg.reply_to_message)
async def forward_any_message(message: types.Message):
    if message.from_user.id == YOUR_TELEGRAM_ID:
        return

    await bot.send_message(
        YOUR_TELEGRAM_ID,
        f"💬 Сообщение от @{message.from_user.username or 'no'} (ID: {message.from_user.id}):\n\n{message.text}"
    )
    await message.answer("✅ Сообщение доставлено продавцу.")

async def main():
    print("✅ Бот запущен. Ожидаю сообщения...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
