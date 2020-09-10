from typing import Iterable

from telegram import ReplyKeyboardMarkup


def get_standard(word_types: Iterable) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        [[item.value for item in word_types]],
        # resize_keyboard=True
    )
