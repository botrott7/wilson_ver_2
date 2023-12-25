from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def create_dictionary_menu_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton(text='Определение слова', callback_data='ru-ru'),
        InlineKeyboardButton(text='Cинонимы слова', callback_data='ru-ru-syn'),
        InlineKeyboardButton(text='Перевод слова с русского на английский', callback_data='ru-en'),
        InlineKeyboardButton(text='Перевод слова с английского на русский', callback_data='en-ru')
    )
    return keyboard
