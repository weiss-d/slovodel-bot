from telegram import ParseMode


def send_welcome_message(bot, chat_id, keyboard, text):
    bot.send_message(chat_id=chat_id,
                     text=text,
                     parse_mode=ParseMode.MARKDOWN_V2,
                     reply_markup=keyboard)


def send_message(bot, chat_id, keyboard, text):
    bot.send_message(chat_id=chat_id,
                     text="<b>{}</b>".format(text),
                     parse_mode=ParseMode.HTML,
                     reply_markup=keyboard)


def send_error_message(bot, chat_id, keyboard, text):
    bot.send_message(chat_id=chat_id,
                     text="⚠ <i>{}</i>".format(text),
                     parse_mode=ParseMode.HTML,
                     reply_markup=keyboard)
