from aiogram import Bot, Dispatcher, types, executor
from config import token
import logging, random
from geopy.geocoders import Nominatim

bot = Bot(token=token)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

geolocator = Nominatim(user_agent="YourBot")

inline_start_buttons = [
    types.InlineKeyboardButton("Получить локацию", callback_data="get_location"),
    types.InlineKeyboardButton("наш сайт", url="https://geeks.kg/")
]
inline_start_keyboard = types.InlineKeyboardMarkup().add(*inline_start_buttons)


@dp.message_handler(commands="start")
async def start(message: types.Message):
    await message.answer(f"Привет, {message.from_user.full_name}", reply_markup=inline_start_keyboard)


@dp.callback_query_handler(lambda call: call.data == "get_location")
async def send_random_location(callback: types.CallbackQuery):
    longitude = random.uniform(-180.000000, 180.000000)
    latitude = random.uniform(-90.000000, 90.000000)

    location = geolocator.reverse((latitude, longitude), language="ru")
    location_name = location.address if location else "Место не найдено"

    await callback.message.answer(f"Высылаю случайное местоположение: {location_name}")
    await callback.message.answer_location(longitude=longitude, latitude=latitude)
    await callback.message.answer(f"Координаты: {latitude} {longitude}")

executor.start_polling(dp, skip_updates=True)
