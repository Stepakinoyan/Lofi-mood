from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.utils import executor
import uvicorn
import requests
import sys
sys.path.append('/mnt/c/Stepa/lofi_mood/code')
from config import TG_TOKEN
sys.path.append('/mnt/c/Stepa/lofi_mood/code/app')
from app import app


bot = Bot(token=TG_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def get_spotify_oauth(message: types.Message):
    await message.answer('test')



# async def send_authorization_notification(message: types.Message):
#     params = {'chat_id': message.chat.id, 'text': 'Авторизация прошла успешно!'}
#     response = requests.post(f'https://api.telegram.org/bot{TG_TOKEN}/sendMessage', params=params)


if __name__ == '__main__':
    uvicorn.run(app, host='localhost', port=8000)
    executor.start_polling(dp, skip_updates=True)
    
