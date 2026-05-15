import logging
import os
import aiohttp
from aiogram import Bot, Dispatcher, types, executor
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TELEGRAM_TOKEN')
RASA_URL = os.getenv('RASA_URL')

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

async def get_rasa_response(user_id: int, text: str):
    payload = {'sender': str(user_id), 'message': text}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(RASA_URL, json=payload) as resp:
                return await resp.json() if resp.status == 200 else None
    except Exception:
        return None

@dp.message_handler(commands=['start', 'restart'])
async def cmd_start(message: types.Message):
    await get_rasa_response(message.from_user.id, '/restart')
    await message.answer('Диалог сброшен. Начнем сначала!')


@dp.message_handler()
async def handle_message(message: types.Message):
    if not message.text: return
    
    responses = await get_rasa_response(message.from_user.id, message.text)
    if responses:
        for response in responses:
            if 'text' in response:
                await message.answer(response['text'])
    else:
        await message.answer('Сервер Rasa недоступен.')

if __name__ == '__main__':
    import asyncio
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    executor.start_polling(dp, skip_updates=True, loop=loop)

