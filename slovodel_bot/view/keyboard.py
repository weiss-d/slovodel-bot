"""
Module for making keyboard markups for Telegram bot chat.
"""
from typing import Iterable

from telegram import ReplyKeyboardMarkup


def get_standard(word_types: Iterable) -> ReplyKeyboardMarkup:
    """Makes plain one-row keyboard from enums and dataclasses."""
    return ReplyKeyboardMarkup(
        [[item.value for item in word_types]],
        # resize_keyboard=True
    )
