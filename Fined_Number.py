import random
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Text, Command

API_KEY : str = ''
bot : Bot = Bot(API_KEY)
dp : Dispatcher = Dispatcher()

users: dict ={}
coun_try: int = 5
def number_1_100() -> int:
    return random.randint(1, 100)

@dp.message(Command(commands=['start']))
async def m_start(message: Message):
    await message.answer('Привет давай сыграем в угадай число!')

    if message.from_user.id not in users:
        users[message.from_user.id] = {'in_game': False, 'count_try': None, 'secret_number': None, 'win': 0, 'all_game': 0}

@dp.message(Command(commands=['help']))
async def m_help(message: Message):
    await message.answer('Игра поставлена таким образом я загадываю число ты его угадываешь')

@dp.message(Command(commands=['stat']))
async def m_stat(message: Message):
    await message.answer(f'Выйграных игр {users[message.from_user.id]["win"]}, всего игр {users[message.from_user.id]["all_game"]}')

@dp.message(Command(commands=['cancel']))
async def m_cancel(message: Message):
    if users[message.from_user.id]['in_game']:
        await message.answer('Вы вышли из игры')
        users[message.from_user.id]['in_game'] = False
    else:
        await message.answer('Мы и так не играем, может сыграем?')

@dp.message(Text(text=['Да', 'Давай', 'Сыграем', 'Игра', 'Играть', 'Хочу играть'], ignore_case=True))
async def m_start_game(message: Message):
    if not users[message.from_user.id]['in_game']:
        await message.answer('Я загадал число от 1 до 100')
        users[message.from_user.id]['in_game'] = True
        users[message.from_user.id]['count_try'] = coun_try
        users[message.from_user.id]['secret_number'] = number_1_100()
    else:
        await message.answer('Мы уже играем')

@dp.message(Text(text=['Нет', 'Не', 'Не хочу', 'Не буду'], ignore_case=True))
async def m_no_game(message: Message):
    if not users[message.from_user.id]['in_game']:
        await message.answer('Жаль, но если захочешь набери команду /start')
    else:
        await message.answer('Мы сейчас играем, жду числа от 1 до 100')

@dp.message(lambda x: x.text and x.text.isdigit() and 1<= int(x.text)<=100)
async def m_nom(message: Message):
    if users[message.from_user.id]['in_game']:
        if int(message.text) == users[message.from_user.id]['secret_number']:
            await message.answer('Ура вы угадали')
            users[message.from_user.id]['win'] += 1
            users[message.from_user.id]['in_game'] = False
            users[message.from_user.id]['all_game'] +=1
        elif int(message.text) > users[message.from_user.id]['secret_number']:
            await message.answer('Мое число меньше')
            users[message.from_user.id]['count_try'] -= 1
        elif int(message.text) < users[message.from_user.id]['secret_number']:
            await message.answer('Мое число больше')
            users[message.from_user.id]['count_try'] -= 1
        if users[message.from_user.id]['count_try'] == 0:
            await message.answer(f'Ваши попытки закончились мое число было {users[message.from_user.id]["secret_number"]}')
            users[message.from_user.id]['in_game'] = False
            users[message.from_user.id]['all_game'] += 1
    else:
        await message.answer('Мы еще не играем сыграем?')

@dp.message()
async def m_any(message: Message):

    if users[message.from_user.id]['in_game']:
        await message.answer('Мы сейчас играем, присылайте числа от 1 до 100')
    else:
        await message.answer('Я ограниченый бот, можем только сыграть')

if __name__ == '__main__':
    dp.run_polling(bot)
