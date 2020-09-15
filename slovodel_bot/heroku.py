"""
Dummy script to run bot on Heroku in webhook mode.

Usage:
    $ python3 heroku.py path_to_config
"""
import os, sys
from pathlib import Path

from slovodel_bot.controller import default_controller
from slovodel_bot import config_parser


def main():
    LISTEN = "0.0.0.0"
    PORT = int(os.environ.get("PORT", "8443"))
    WEBHOOK_URL = "https://" + os.environ.get("HEROKU_APP_NAME") + ".herokuapp.com/"

    config_file = Path(sys.argv[1])
    ctrl = default_controller.defaultController(config_parser.get_dataclass(config_file))

    ctrl.start_bot_webhook(listen=LISTEN,
                        port=PORT,
                        webhook_url=WEBHOOK_URL,
                        )


if __name__ == "__main__":
    main()
