from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def create_dictionary_menu_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton(text='Определение слова', callback_data='ru-ru'),
        InlineKeyboardButton(text='Перевод с русского на английский', callback_data='ru-en'),
        InlineKeyboardButton(text='Перевод с английского на русский', callback_data='en-ru')
    )
    return keyboard
