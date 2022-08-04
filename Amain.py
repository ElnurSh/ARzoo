import aiogram.types
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
start_btn = InlineKeyboardMarkup().add(order_btn).row(next_btn)
middle_btn = InlineKeyboardMarkup().add(order_btn).row(back_btn, next_btn)
end_btn = InlineKeyboardMarkup().add(order_btn).row(back_btn)



@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await bot.send_photo(message.chat.id, photo=open('1.jpg', 'rb'), caption='Hello! Write me something! 1', reply_markup=start_btn)


@dp.callback_query_handler(text='next')
async def next_photo(call: types.CallbackQuery):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    await bot.send_photo(call.message.chat.id, photo=open('2.jpg', 'rb'), caption='Hello! Write me something! 2', reply_markup=middle_btn)


if __name__ == '__main__':
    executor.start_polling(dp)