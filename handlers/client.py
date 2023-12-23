from config.config import bot
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from model.OpenAI import message_AI, message_URL
from logibot.loggerbot import logger


class Form_bot(StatesGroup):
    bot_command = State()
    url_command = State()


REPLIC_EXCEPT_CLIENT = 'Пожалуйста, повторите попытку позже или обратитесь за помощью к администратору.'


async def command_start(message: types.Message):
    '''Функция, которая запускает бота'''
    try:
        await bot.send_message(message.from_user.id, 'Hello this is commadn start!')
        await message.delete()
    except Exception as e:
        logger.exception(f'Произошла ошибка: {str(e)}')
        await message.answer(REPLIC_EXCEPT_CLIENT)


async def command_help(message: types.Message):
    '''Команда, которая вызывает список доступных команд'''
    try:
        await message.answer('THIS IS TEST COMMAND HELP')
        await message.delete()
    except Exception as e:
        logger.exception(f'Произошла ошибка: {str(e)}')
        await message.answer(REPLIC_EXCEPT_CLIENT)


async def command_finance(message: types.Message):
    '''Finance command'''
    try:
        await message.answer('This is FINANCE COMMAND')
    except Exception as e:
        logger.exception(f'Произошла ошибка: {str(e)}')
        await message.answer(REPLIC_EXCEPT_CLIENT)


async def command_bot(message: types.Message, state: FSMContext):
    '''Команда, которая просит пользователя ввести вопрос'''
    try:
        await message.answer('Пожалуйста, введите ваш вопрос: ')
        await Form_bot.bot_command.set()
    except Exception as e:
        logger.exception(f'Произошла ошибка: {str(e)}')
        await message.answer(REPLIC_EXCEPT_CLIENT)


async def proccess_question_bot(message: types.Message, state: FSMContext):
    '''Ожидание и генерация ответа'''
    try:
        question = message.text
        result = await message_AI(question)
        await message.answer(f'Ответ на ваш вопрос: {result}')
        await state.finish()
    except Exception as e:
        logger.exception(f'Произошла ошибка: {str(e)}')
        await message.answer(REPLIC_EXCEPT_CLIENT)


async def command_url(message: types.Message, state: FSMContext):
    '''URL command : позволяет получить информацию о сайте с помощью агента HfAgent'''
    try:
        await message.answer('Пожалуйста, введите сайт:')
        await Form_bot.url_command.set()
    except Exception as e:
        logger.exception(f'Произошла ошибка: {str(e)}')
        await message.answer(REPLIC_EXCEPT_CLIENT)


async def process_question_url(message: types.Message, state: FSMContext):
    '''Ожидание урла и генерация ответа'''
    try:
        question = message.text
        result = await message_URL(question)
        await message.answer(f'Ответ: {result}')
        await state.finish()
    except Exception as e:
        logger.exception(f'Произошла ошибка: {str(e)}')
        await message.answer(REPLIC_EXCEPT_CLIENT)


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start'])
    dp.register_message_handler(command_help, commands=['help'])
    dp.register_message_handler(command_finance, commands=['finance'])
    dp.register_message_handler(command_bot, commands=['bot'], state='*')
    dp.register_message_handler(proccess_question_bot, state=Form_bot.bot_command)
    dp.register_message_handler(command_url, commands=['url'], state='*')
    dp.register_message_handler(process_question_url, state=Form_bot.url_command)
