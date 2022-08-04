from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pymongo import MongoClient
from config import *
import certifi


cluster = MongoClient(MongoTOKEN, tlsCAFile=certifi.where())
db = cluster["Bot"]
quiz = db["Quiz"]

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


#https://surik00.gitbooks.io/aiogram-lessons/content/chapter5.html

order_btn = InlineKeyboardButton('🛍 Sifariş et!', callback_data='order')
back_btn = InlineKeyboardButton('🔙 Geri', callback_data='back')
next_btn = InlineKeyboardButton('Növbəti ➡️', callback_data='next')
btn2 = InlineKeyboardMarkup().add(order_btn).row(next_btn) # order order and next row button
btn3 = InlineKeyboardMarkup().add(order_btn).row(back_btn, next_btn) # order button and back, next row buttons



@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await bot.send_message(message.from_user.id,"Hello! Write me something!",reply_markup=btn2)


if __name__ == '__main__':
    executor.start_polling(dp)
