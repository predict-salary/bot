import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import aiohttp
import re

API_TOKEN = '7118408474:AAFdVDWoRXgu1IZ6JIsLR0434DT3IBNX99I'
BACKEND_URL = 'http://localhost:8000/api/v1/inference'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot=bot)


@dp.message(Command('start'))
async def start(message: types.Message):
    await message.reply(
        "Привет! Я бот, который поможет тебе спрогнозировать заработную плату вакансии методами машинного обучения.\n"
        "Отправь мне ссылку на вакансию с сайта hh.ru")


@dp.message()
async def process_message(message: types.Message):
    hh_pattern = re.compile(r'https://hh\.ru/vacancy/\d+')

    if hh_pattern.match(message.text):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(BACKEND_URL, json={"url": message.text}) as response:
                    backend_response = await response.json()
            if backend_response["salary_from"] is None:
                await message.reply("Не могу даже предположить заработную плату...")
            elif backend_response["salary_to"] is None:
                await message.reply(f"Твоя зарплата от {backend_response['salary_from']} и ей нету конца!")
            else:
                await message.reply(f"Твоя зарплата от {backend_response['salary_from']} до {backend_response['salary_to']}!")


            # await message.reply(f"{backend_response}")
        except Exception as e:
            print(e)
            await message.reply("Ошибка запроса")
    else:
        await message.reply("Упс! Похоже, эта ссылка не ведет к вакансии на hh.ru. Попробуйте еще раз.")

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    import asyncio

    asyncio.run(main())
