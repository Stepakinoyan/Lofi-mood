from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import sys
sys.path.append('/mnt/c/Stepa/lofi_mood/code')
from app.parser.lofi import Recommendations
from app.config import TG_TOKEN

bot = Bot(token=TG_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
        await message.answer(f'Hello, {message.from_user.first_name}! Please, write one of the commands: Sad, calm, happy. For example: /sad')

@dp.message_handler(commands=['sad'])
async def commands(message: types.Message):
        sp = Recommendations('sad')
        lofi_json = await sp.get_lofi()
        for i in lofi_json:
                await message.answer(f"{i.get('title')} - {i.get('href')}")

@dp.message_handler(commands=['calm'])
async def commands(message: types.Message):
        sp = Recommendations('calm')
        lofi_json = await sp.get_lofi()
        for i in lofi_json:
                await message.answer(f"{i.get('title')} - {i.get('href')}")

@dp.message_handler(commands=['happy'])
async def commands(message: types.Message):
        sp = Recommendations('happy')
        lofi_json = await sp.get_lofi()
        for i in lofi_json:
                await message.answer(f"{i.get('title')} - {i.get('href')}")



if __name__ == '__main__':
        executor.start_polling(dp)