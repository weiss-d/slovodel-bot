"""
Main script to acquire the configuration, instantiate and run Controller.
"""
from pathlib import Path

import click

from slovodel_bot.controller import default_controller
from slovodel_bot import config_parser


DEFAULT_CONFIG_PATH = "bot_config.toml"


@click.command()
@click.argument("config_path", type=click.Path("rt"), nargs=-1)
def main(config_path) -> None:
    """Instanciate controller and run bot."""
    config_file = Path(config_path[0]) if config_path else Path(DEFAULT_CONFIG_PATH)
    try:
        config = config_parser.get_dataclass(config_file)
    except:
        print("Configuration file error:")
        raise click.ClickException(str(e))

    ctrl = default_controller.defaultController(config)
    ctrl.start_bot()


if __name__ == "__main__":
    main()
