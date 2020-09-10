"""
A collection of functions to send different types of bot messages in corresponding format.
"""
from telegram import ParseMode
from telegram.utils.helpers import escape_markdown


def send_welcome_message(bot, chat_id, keyboard, text):
    bot.send_message(
        chat_id=chat_id,
        text=escape_markdown(text, version=2),
        parse_mode=ParseMode.MARKDOWN_V2,
        reply_markup=keyboard,
    )


def send_message(bot, chat_id, keyboard, text):
    bot.send_message(
        chat_id=chat_id,
        text="<b>{}</b>".format(text),
        parse_mode=ParseMode.HTML,
        reply_markup=keyboard,
    )


def send_error_message(bot, chat_id, keyboard, text):
    bot.send_message(
        chat_id=chat_id,
        text="⚠ <i>{}</i>".format(text),
        parse_mode=ParseMode.HTML,
        reply_markup=keyboard,
    )
