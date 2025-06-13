from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command

API_TOKEN : str = ''

bot : Bot = Bot(token=API_TOKEN)
dp : Dispatcher = Dispatcher()

@dp.message(Command(commands=['start']))
async def m_star(message : Message):
    await message.answer('Привет я Эхо Бот')

@dp.message(Command(commands=['help']))
async def m_help(message : Message):
    await message.answer('Я буду повторять за тобой все сообщения которые ты напишешь')

@dp.message()
async def m_all(message : Message):
    print(message.json(indent=4, exclude_none=True))
    try:
        await message.send_copy(chat_id=message.chat.id)
    except:
        await message.answer('Данный тип сообщения не потдерживается методом send_copy')

if __name__ == '__main__':
    dp.run_polling(bot)
