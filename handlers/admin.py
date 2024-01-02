import aiohttp

from config.config import ADMIN_IDS, CATEGORY_VALUES
from aiogram.dispatcher import FSMContext
from aiogram import types, Dispatcher
from keyboards_inline.ink_api_admin import make_inline_keyboard_for_categories
from aiogram.dispatcher.filters.state import State, StatesGroup
from logibot.loggerbot import logger


class Form(StatesGroup):
    category = State()
    activity = State()


REPLIC_EXCEPT_CLIENT = 'Произошла ошибка.'
REPLIC_NO_AUTH = 'Извините, вы не авторизованы для использования этой команды'


async def command_admin(message: types.Message):
    '''Вызывет список команд доступных администратору'''
    try:
        admin_id = ADMIN_IDS  # Замените на админский айди
        if int(message.from_user.id) == int(admin_id):
            await message.answer('This is ADMIN COMMAND')
        else:
            await message.answer(REPLIC_NO_AUTH)
    except Exception as e:
        logger.exception(f'Произошла ошибка: {str(e)}')
        await message.answer(REPLIC_EXCEPT_CLIENT)


async def command_post_api(message: types.Message):
    '''POST API command handler'''
    try:
        admin_id = ADMIN_IDS
        if int(message.from_user.id) == int(admin_id):
            categories = ['PH', 'ID', 'CG', 'DT', 'PG']
            keyboard = make_inline_keyboard_for_categories(categories)
            await Form.category.set()
            await message.answer("Select a category", reply_markup=keyboard)
        else:
            await message.answer(REPLIC_NO_AUTH)
    except Exception as e:
        logger.exception(f'Произошла ошибка: {str(e)}')
        await message.answer(REPLIC_EXCEPT_CLIENT)


async def command_get_api(message: types.Message):
    '''GET API command handler'''
    try:
        admin_id = ADMIN_IDS
        if int(message.from_user.id) == int(admin_id):
            measurements = await get_measurements()
            if measurements is not None:
                result = ""
                for measurement in measurements:
                    result += f"Category: {measurement['category']}, Activity: {measurement['activity']}, Value: {measurement['value']}\n"
                await message.answer(result)
            else:
                await message.answer('Не удалось получить GET-запрос')
        else:
            await message.answer(REPLIC_NO_AUTH)
    except Exception as e:
        logger.exception(f'Произошла ошибка: {str(e)}')
        await message.answer(REPLIC_EXCEPT_CLIENT)


async def get_measurements():
    '''Get all measurements'''
    try:
        async with aiohttp.ClientSession() as session:
            response = await session.get('http://127.0.0.1:8000/api/measurements/')  # Указать ваш API
            logger.info('GET', response.status)
            if response.status == 200:
                measurements = await response.json()
                return measurements
            else:
                return None
    except Exception as e:
        logger.exception(f'Произошла ошибка: {str(e)}')
        return None


async def callback_query_handler(callback_query: types.CallbackQuery, state: FSMContext):
    """Обработка callback_query для выбора категории"""
    try:
        await Form.category.set()
        await process_category(callback_query, state)
    except Exception as e:
        logger.exception(f'Произошла ошибка: {str(e)}')
        await callback_query.answer(REPLIC_EXCEPT_CLIENT)


async def process_category(callback_query: types.CallbackQuery, state: FSMContext):
    """Обработка выбранной категории"""
    try:
        await callback_query.answer()
        user_category = callback_query.data
        if user_category in CATEGORY_VALUES:
            await state.update_data(category=user_category)
            await Form.next()
            await callback_query.message.answer("Enter your activity")
    except Exception as e:
        logger.exception(f'Произошла ошибка: {str(e)}')
        await callback_query.answer(REPLIC_EXCEPT_CLIENT)


async def process_activity(message: types.Message, state: FSMContext):
    """Обработка полученной активности"""
    try:
        await state.update_data(activity=message.text)
        user_data = await state.get_data()
        category = user_data.get('category')
        value = CATEGORY_VALUES[category]
        activity = user_data.get('activity')

        async with aiohttp.ClientSession() as session:  # Отправка данных через API
            payload = {
                "category": category,
                "value": value,
                "activity": activity,
            }
            async with session.post('http://127.0.0.1:8000/api/measurements/',
                                    json=payload) as response:  # Указать ваш API
                logger.info('POST', response.status)
                if response.status == 200:
                    await message.answer(f"Successfully sent data: {category} - {value} - {activity}")
                else:
                    await message.answer(f"Не удалось получить POST-запрос: {response.status}")
        await message.answer(f"Data sent: {category} - {value} - {activity}")
        await state.finish()
    except Exception as e:
        logger.exception(f'Произошла ошибка: {str(e)}')
        await message.answer(REPLIC_EXCEPT_CLIENT)


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(command_admin, commands=['admin'])
    dp.register_message_handler(command_get_api, commands=['get_api'])
    dp.register_message_handler(command_post_api, commands=['post_api'])
    dp.register_callback_query_handler(callback_query_handler,
                                       lambda c: c.data in CATEGORY_VALUES,
                                       state=Form.category)
    dp.register_message_handler(process_activity, state=Form.activity)
