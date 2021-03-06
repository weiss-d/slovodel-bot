"""
Controller module to be used in default mode.
"""
from dataclasses import dataclass
from pathlib import Path
import re

from telegram import ReplyKeyboardMarkup
from telegram.ext import (
    CommandHandler,
    Filters,
    MessageHandler,
    Updater,
)

from slovodel_bot.model import word_maker
from slovodel_bot.view import keyboard, message_sender


@dataclass
class Configuration:
    """Controller config."""
    bot_token: str
    welcome_message_file: Path
    word_maker_config: word_maker.Configuration


class defaultController:
    """Main controller class."""
    bot: Updater
    kbd_markup: ReplyKeyboardMarkup
    configuration: Configuration
    welcome_message: str

    def __init__(self, configuration: Configuration) -> None:
        # Preparing the bot
        self.configuration = configuration
        self.bot = Updater(token=self.configuration.bot_token, use_context=True)
        self.bot.dispatcher.add_handler(CommandHandler("start", self.__cmd_start))
        self.bot.dispatcher.add_handler(
            MessageHandler(
                Filters.text & Filters.regex(self._get_word_type_regex()),
                self.__msg_word_type,
            )
        )
        self.bot.dispatcher.add_handler(MessageHandler(Filters.text, self.__msg_other))
        self.kbd_markup = keyboard.get_standard(word_maker.wordTypes)
        # Preparing everything else
        self.slovodel = word_maker.Slovodel(self.configuration.word_maker_config)
        with self.configuration.welcome_message_file.open() as file:
            self.welcome_message = file.read()

    def _get_word_type_regex(self) -> re.compile:
        """Make a regex for message filter."""
        pattern = []
        for wtype in word_maker.wordTypes:
            pattern.append(r"(\A" + wtype.value + r"\Z)")
        return re.compile("|".join(pattern))

    def start_bot(self) -> None:
        """Start the initialized bot in polling mode."""
        self.bot.start_polling()
        self.bot.idle()

    def start_bot_webhook(self, listen: str, port: int, webhook_url: str) -> None:
        """Start the initialized bot in webhook mode."""
        self.bot.start_webhook(listen=listen,
                               port=port,
                               url_path=self.configuration.bot_token,
                               )
        self.bot.bot.set_webhook(webhook_url + self.configuration.bot_token)
        self.bot.idle()


    # Command Handlers

    def __cmd_start(self, update, context):
        message_sender.send_welcome_message(
            context.bot, update.effective_chat.id, self.kbd_markup, self.welcome_message
        )

    # Message Handlers

    def __msg_word_type(self, update, context):
        try:
            reply_word = self.slovodel.make_unique_word(
                word_maker.wordTypes(context.match.string)
            )
            message_sender.send_message(
                context.bot, update.effective_chat.id, self.kbd_markup, reply_word
            )
        except ValueError:
            message_sender.send_error_message(
                context.bot,
                update.effective_chat.id,
                self.kbd_markup,
                "Что-то пошло не так...",
            )

    def __msg_other(self, update, context):
        message_sender.send_error_message(
            context.bot,
            update.effective_chat.id,
            self.kbd_markup,
            "Не понимаю ваш запрос. Воспользуйтесь одной из кнопок внизу.",
        )
