from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from time import sleep
from pymongo import MongoClient
from config import *
import certifi


cluster = MongoClient(MongoTOKEN, tlsCAFile=certifi.where())
db = cluster["Bot"]
shop = db["arzoo"]

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
    try:
        shop.delete_one({'user': message.from_user.id})
    except:
        pass
    shop.insert_one({'user': message.from_user.id, 'photo': 0, 'phone': 0})
    shop.update_one({'user': message.from_user.id},
                    {'$set': {'photo': int(shop.find({'user': message.from_user.id}).distinct('photo')[-1]) + 1}})
    await bot.send_photo(message.chat.id, photo=open(f"{shop.find({'user': message.from_user.id}).distinct('photo')[-1]}.jpg", 'rb'), caption='Hello! Write me something! 1', reply_markup=start_btn)



@dp.callback_query_handler(text='next')
async def next_photo(call: types.CallbackQuery):
    if shop.find({'user': call.from_user.id}).distinct('photo')[-1] == 1:
        shop.update_one({'user': call.from_user.id},
                        {'$set': {'photo': int(shop.find({'user': call.from_user.id}).distinct('photo')[-1]) + 1}})
        await bot.delete_message(call.from_user.id, call.message.message_id)
        await bot.send_photo(call.message.chat.id, photo=open(f"{shop.find({'user': call.from_user.id}).distinct('photo')[-1]}.jpg", 'rb'), caption="Hello! Write me something! 3", reply_markup=middle_btn)
    elif shop.find({'user': call.from_user.id}).distinct('photo')[-1] == 2:
        shop.update_one({'user': call.from_user.id},
                        {'$set': {'photo': int(shop.find({'user': call.from_user.id}).distinct('photo')[-1]) + 1}})
        await bot.delete_message(call.from_user.id, call.message.message_id)
        await bot.send_photo(call.message.chat.id, photo=open(f"{shop.find({'user': call.from_user.id}).distinct('photo')[-1]}.jpg", 'rb'), caption="Hello! Write me something! 3", reply_markup=middle_btn)
    elif shop.find({'user': call.from_user.id}).distinct('photo')[-1] == 3:
        shop.update_one({'user': call.from_user.id},
                        {'$set': {'photo': int(shop.find({'user': call.from_user.id}).distinct('photo')[-1]) + 1}})
        await bot.delete_message(call.from_user.id, call.message.message_id)
        await bot.send_photo(call.message.chat.id, photo=open(f"{shop.find({'user': call.from_user.id}).distinct('photo')[-1]}.jpg", 'rb'), caption="Hello! Write me something! 3", reply_markup=end_btn)


@dp.callback_query_handler(text='back')
async def previous_photo(call: types.CallbackQuery):
    if shop.find({'user': call.from_user.id}).distinct('photo')[-1] <= 4 or shop.find({'user': call.from_user.id}).distinct('photo')[-1] >= 2:
        if shop.find({'user': call.from_user.id}).distinct('photo')[-1] == 2:
            await bot.delete_message(call.from_user.id, call.message.message_id)
            shop.update_one({'user': call.from_user.id},
                        {'$set': {'photo': int(shop.find({'user': call.from_user.id}).distinct('photo')[-1]) - 1}})
            await bot.send_photo(call.message.chat.id,
                             photo=open(f"{shop.find({'user': call.from_user.id}).distinct('photo')[-1]}.jpg", 'rb'),
                             caption="Hello! Write me something! 2", reply_markup=start_btn)
        else:
            await bot.delete_message(call.from_user.id, call.message.message_id)
            shop.update_one({'user': call.from_user.id},
                        {'$set': {'photo': int(shop.find({'user': call.from_user.id}).distinct('photo')[-1]) - 1}})
            await bot.send_photo(call.message.chat.id, photo=open(f"{shop.find({'user': call.from_user.id}).distinct('photo')[-1]}.jpg", 'rb'), caption="Hello! Write me something! 2", reply_markup=middle_btn)


if __name__ == '__main__':
    executor.start_polling(dp)