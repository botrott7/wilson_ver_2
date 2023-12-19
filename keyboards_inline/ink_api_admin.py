from typing import List
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def make_inline_keyboard_for_categories(categories: List[str]) -> InlineKeyboardMarkup:
    """Key для post-api"""
    kb = InlineKeyboardMarkup(row_width=2)
    for category in categories:
        kb.insert(InlineKeyboardButton(category, callback_data=category))
    return kb
