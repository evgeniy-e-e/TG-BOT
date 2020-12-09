import logging
import os
import asyncio
from datetime import datetime
from aiogram import Bot, Dispatcher, executor, types
from sqlighter import SQLighter
from dotenv import load_dotenv, find_dotenv
from imdb_trailers import IMDB


load_dotenv(find_dotenv())

API_TOKEN = os.getenv('TG_API_KEY')

# задаем уровень логов
logging.basicConfig(level=logging.INFO)

# инициализируем бота
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# инициализируем соединение с бд
db = SQLighter('db.db')

# инициализируем парсер
imdb_parse = IMDB('lastkey.txt')


# команда активации подписки
@dp.message_handler(commands=['subscribe'])
async def subscribe(message: types.Message):
    if(not db.subscriber_exist(message.from_user.id)):
        # если юзера нет в базе, то добавляем его
        db.add_subscriber(message.from_user.id)
    else:
        # если есть, обновляем статус подписки
        db.update_subscriptions(message.from_user.id, True)

    await message.answer("Вы успешно подписались на рассылку!\nЖдите, скоро выйдут новые обзоры и вы узнаете  о них первым")


# команда отписки
@dp.message_handler(commands=['unsubscribe'])
async def subscribe(message: types.Message):
    if(not db.subscriber_exist(message.from_user.id)):
        # если юзера нет в базе, то добавляем его с неактивной подпиской(запоминаем)
        db.add_subscriber(message.from_user.id, False)
        await message.answer("Вы итак не подписаны.")
    else:
        # если есть, обновляем статус подписки
        db.update_subscriptions(message.from_user.id, False)
        await message.answer("Вы успешно подписались от рассылку!")

# проверяем наличие новых трейлеров и делаем рассылку
async def check_new(wait_for):
    while True:
        await asyncio.sleep(wait_for)
        # проверка новых трейлеров
        new_trailers = imdb_parse.new_trailers()
        if new_trailers:
            # если трейлеры есть переворачиваем список и итерируем
            new_trailers.reverse()
            for nt in new_trailers:
                nfo = imdb_parse.trailer_info(nt)
            # получаем список подписчиков
            subscriptions = db.get_subscriptions()

            # отправляем всем новость
            with open (imdb_parse.download_image(nfo['image']), 'rb') as photo:
                for s in subscriptions:
                    await  bot.send_photo(
                        s[1],
                        photo,
                        caption = nfo['title'] + "\n" + nfo['link'],
                        disable_notification = True
                    )
            # обговляем ключ
            imdb_parse.update_lastkey('id')



if __name__ == '__main__':
    dp.loop.create_task(check_new(10))
    executor.start_polling(dp, skip_updates=False)