from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from time import ctime
from product_name import names
from pymongo import MongoClient
from config import *
import certifi

cluster = MongoClient(MongoTOKEN, tlsCAFile=certifi.where())
db = cluster["Bot"]
shop = db["arzoo"]

bot = Bot(token=MySimpleQuizBot)
dp = Dispatcher(bot)

# https://surik00.gitbooks.io/aiogram-lessons/content/chapter5.html
order_btn = InlineKeyboardButton('🛍 Sifariş et!', callback_data='order')
back_btn = InlineKeyboardButton('🔙 Geri', callback_data='back')
next_btn = InlineKeyboardButton('Növbəti ➡️', callback_data='next')
start_btn = InlineKeyboardMarkup().add(order_btn).row(next_btn)
middle_btn = InlineKeyboardMarkup().add(order_btn).row(back_btn, next_btn)
end_btn = InlineKeyboardMarkup().add(order_btn).row(back_btn)
markup_request = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(
    KeyboardButton('Əlaqə nömrəmi göndər ☎️', request_contact=True))
# *****************************************************************
#-1001773224811
@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    try:
        shop.delete_one({'user': message.from_user.id})
    except:
        pass
    shop.insert_one(
        {'user': message.from_user.id, 'last_visit': ctime(), 'photo': 0, 'phone': 0, 'product': 0, 'order_time': 0})
    shop.update_one({'user': message.from_user.id},
                    {'$set': {'photo': int(shop.find({'user': message.from_user.id}).distinct('photo')[-1]) + 1}})
    await bot.send_photo(message.chat.id,
                         photo=open(f"{shop.find({'user': message.from_user.id}).distinct('photo')[-1]}.jpg", 'rb'),
                         caption=names[shop.find({'user': message.from_user.id}).distinct('photo')[-1]],
                         reply_markup=start_btn)


@dp.callback_query_handler(text='next')
async def next_photo(call: types.CallbackQuery):
    if shop.find({'user': call.from_user.id}).distinct('photo')[-1] >= 1 or \
            shop.find({'user': call.from_user.id}).distinct('photo')[-1] <= 3:
        if shop.find({'user': call.from_user.id}).distinct('photo')[-1] == 3:
            shop.update_one({'user': call.from_user.id},
                            {'$set': {'photo': int(shop.find({'user': call.from_user.id}).distinct('photo')[-1]) + 1}})
            await bot.delete_message(call.from_user.id, call.message.message_id)
            await bot.send_photo(call.message.chat.id,
                                 photo=open(f"{shop.find({'user': call.from_user.id}).distinct('photo')[-1]}.jpg",
                                            'rb'),
                                 caption=names[shop.find({'user': call.from_user.id}).distinct('photo')[-1]],
                                 reply_markup=end_btn)
        else:
            shop.update_one({'user': call.from_user.id},
                            {'$set': {'photo': int(shop.find({'user': call.from_user.id}).distinct('photo')[-1]) + 1}})
            await bot.delete_message(call.from_user.id, call.message.message_id)
            await bot.send_photo(call.message.chat.id,
                                 photo=open(f"{shop.find({'user': call.from_user.id}).distinct('photo')[-1]}.jpg",
                                            'rb'),
                                 caption=names[shop.find({'user': call.from_user.id}).distinct('photo')[-1]],
                                 reply_markup=middle_btn)


@dp.callback_query_handler(text='back')
async def previous_photo(call: types.CallbackQuery):
    if shop.find({'user': call.from_user.id}).distinct('photo')[-1] <= 4 or \
            shop.find({'user': call.from_user.id}).distinct('photo')[-1] >= 2:
        if shop.find({'user': call.from_user.id}).distinct('photo')[-1] == 2:
            await bot.delete_message(call.from_user.id, call.message.message_id)
            shop.update_one({'user': call.from_user.id},
                            {'$set': {'photo': int(shop.find({'user': call.from_user.id}).distinct('photo')[-1]) - 1}})
            await bot.send_photo(call.message.chat.id,
                                 photo=open(f"{shop.find({'user': call.from_user.id}).distinct('photo')[-1]}.jpg",
                                            'rb'),
                                 caption=names[shop.find({'user': call.from_user.id}).distinct('photo')[-1]],
                                 reply_markup=start_btn)
        else:
            await bot.delete_message(call.from_user.id, call.message.message_id)
            shop.update_one({'user': call.from_user.id},
                            {'$set': {'photo': int(shop.find({'user': call.from_user.id}).distinct('photo')[-1]) - 1}})
            await bot.send_photo(call.message.chat.id,
                                 photo=open(f"{shop.find({'user': call.from_user.id}).distinct('photo')[-1]}.jpg",
                                            'rb'),
                                 caption=names[shop.find({'user': call.from_user.id}).distinct('photo')[-1]],
                                 reply_markup=middle_btn)


@dp.callback_query_handler(text='order')
async def user_order(call: types.CallbackQuery):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    await bot.send_message(call.message.chat.id, "📱 Sifarişi tamamlamaq üçün əlaqə \nnömrənizi göndərməyiniz şərtdir❗",
                           reply_markup=markup_request)


@dp.message_handler(content_types=['contact'])
async def contact(message):
    if message.contact is not None:
        await bot.send_message(message.chat.id, '🥳 Sifarişiniz tamamlandı❗\n'
                                                'Sizinlə qısa zamanda əlaqə saxlayarıq❗\n\n'
                                                '☝️Yenidən sifariş etmək üçün <b>/start</b> göndərməyiniz yetərlidir.',
                               parse_mode='HTML')
        shop.update_one({'user': message.contact.user_id},
                        {'$set': {'phone': message.contact.phone_number,
                                  'product': names[shop.find({'user': message.from_user.id}).distinct('photo')[-1]],
                                  'order_time': ctime()}})
        await bot.send_message(channel_id, f"Sifarişçi: <b>{message.contact.first_name}</b>\n"
                                           f"Əlaqə nömrəsi: <b>{message.contact.phone_number}</b>\n"
                                           f"Məhsulun kodu: <b>{shop.find({'user': message.from_user.id}).distinct('photo')[-1]}</b>\n"
                                           f"Məhsulun adı: <b>{shop.find({'user': message.from_user.id}).distinct('product')[-1]}</b>",
                               parse_mode='HTML')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
