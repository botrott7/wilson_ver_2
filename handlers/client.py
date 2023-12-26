from config.config import bot, PROCESSOR, MODEL
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from keyboards_inline.ink_client import create_dictionary_menu_keyboard
from model.OpenAI import message_AI
from logibot.loggerbot import logger
from langs.langs_func import translate_word
import aiohttp
from io import BytesIO
from PIL import Image
from validators import url as validate_url

class Form_bot(StatesGroup):
    BOT_COMMAND = State()
    WAITING_FOR_WORD = State()
    IMAGE_FOR_DESC = State()


REPLIC_EXCEPT_CLIENT = 'Пожалуйста, повторите попытку позже или обратитесь за помощью к администратору.'

async def command_start(message: types.Message):
    '''Команда для запуска бота'''
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


async def command_image(message: types.Message, state: FSMContext):
    '''Команда, которая дает опиание изображению'''
    try:
        await message.answer('Пожалуйста, введите URL изображения или прикрепите изображение(поставьте галочку' + ' ☑ ' + 'Сжать изображение): ')
        await Form_bot.IMAGE_FOR_DESC.set()
    except Exception as e:
        logger.exception(f'Произошла ошибка: {str(e)}')
        await message.answer("Произошла ошибка. Попробуйте ещё раз.")


async def image_handler(message: types.Message, state: FSMContext):
    '''Обработка и генерация ответа по изображению'''
    if message.photo:
        photo = message.photo[-1]
        image_data = BytesIO()
        await photo.download(destination_file=image_data)  # Передача BytesIO объекта как destination_file
        image_data.seek(0)  # Перемещение курсора в начало файла
        raw_image = Image.open(image_data).convert('RGB')
    elif message.text and validate_url(message.text):  # Проверка URL на корректность
        img_url = message.text
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(img_url) as response:
                    if response.status == 200:
                        image_data = BytesIO(await response.read())
                        raw_image = Image.open(image_data).convert('RGB')
                    else:
                        await message.reply("Невозможно загрузить изображение по указанному URL.")
                        return
            except Exception as e:
                await message.reply("Ошибка загрузки изображения.")
                logger.exception(f'Произошла ошибка: {str(e)}')
                return
    else:
        await message.reply("Пожалуйста, прикрепите изображение или отправьте URL изображения.")
        return

    await generate_caption(message, raw_image)

    await state.finish()  # Сброс состояния после обработки изображения


async def generate_caption(message: types.Message, raw_image: Image.Image):
    """Генерирует подпись для обработанного изображения"""
    try:
        text = "a photography of"
        inputs = PROCESSOR(raw_image, text, return_tensors="pt")
        out = MODEL.generate(**inputs)
        caption = PROCESSOR.decode(out[0], skip_special_tokens=True)
        await message.answer(caption)
    except Exception as e:
        logger.exception(f"Ошибка при генерации подписи: {e}")
        await message.answer("Произошла ошибка при обработке изображения.")


async def command_bot(message: types.Message, state: FSMContext):
    '''Команда, для генерации ответа от модели, просит пользователя ввести вопрос'''
    try:
        await message.answer('Пожалуйста, введите ваш вопрос: ')
        await Form_bot.BOT_COMMAND.set()
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


async def command_langs(message: types.Message, state: FSMContext):
    '''Команда, позволяет провести определенные действия со словом'''
    try:
        keyboard = create_dictionary_menu_keyboard()
        await message.reply("Выберите режим:", reply_markup=keyboard)
        await Form_bot.WAITING_FOR_WORD.set()
    except Exception as e:
        logger.exception(f'Произошла ошибка: {str(e)}')
        await message.answer(REPLIC_EXCEPT_CLIENT)


async def proccess_command_langs(callback_query: types.CallbackQuery, state: FSMContext):
    '''Ожидаение ввода слова'''
    try:
        lang = callback_query.data
        await state.update_data(lang=lang)
        await bot.send_message(chat_id=callback_query.from_user.id, text='Введите слово: ')
    except Exception as e:
        logger.exception(f'Произошла ошибка: {str(e)}')
        await callback_query.answer(REPLIC_EXCEPT_CLIENT)


async def proccess_command_word(message: types.Message, state: FSMContext):
    '''Обработка и запуск функции для взаимодействия с API'''
    try:
        lang = (await state.get_data()).get('lang')
        text = message.text
        result = await translate_word(lang, text)
        await message.reply(f'Ваш ответ: {result}')
        await state.finish()
    except Exception as e:
        logger.exception(f'Произошла ошибка: {str(e)}')
        await message.answer(REPLIC_EXCEPT_CLIENT)


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start'])
    dp.register_message_handler(command_help, commands=['help'])
    dp.register_message_handler(command_image, commands=['image'], state='*')
    dp.register_message_handler(image_handler, content_types=['photo', 'text'], state=Form_bot.IMAGE_FOR_DESC)
    dp.register_message_handler(command_bot, commands=['bot'], state='*')
    dp.register_message_handler(command_langs, commands=['langs'], state='*')
    dp.register_callback_query_handler(proccess_command_langs, state=Form_bot.WAITING_FOR_WORD)
    dp.register_message_handler(proccess_command_word, state=Form_bot.WAITING_FOR_WORD)
    dp.register_message_handler(proccess_question_bot, state=Form_bot.BOT_COMMAND)
