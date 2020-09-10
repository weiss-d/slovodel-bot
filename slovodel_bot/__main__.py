"""
Main script to acquire the configuration, instantiate and run Controller.
"""
from pathlib import Path

import click
import dacite
import toml

from slovodel_bot.controller import default_controller
from slovodel_bot.model.word_maker import wordTypes


DEFAULT_CONFIG_PATH = "bot_config.toml"


def get_config(file: click.Path) -> default_controller.Configuration:
    """Parse config file to controller.Configuration dataclass."""
    converters = {
        Path: Path,
        wordTypes: lambda x: wordTypes.__members__.get(x),
    }
    try:
        with open(file) as config:
            toml_config = toml.load(config)

        return dacite.from_dict(
            data_class=default_controller.Configuration,
            data=toml_config,
            config=dacite.Config(type_hooks=converters),
        )
    except Exception as e:
        print("Configuration file error:")
        raise click.ClickException(str(e))


@click.command()
@click.argument("config", type=click.Path("rt"), nargs=-1)
def main(config) -> None:
    """Instanciate controller and run bot."""
    config_file = Path(config[0]) if config else Path(DEFAULT_CONFIG_PATH)
    ctrl = default_controller.defaultController(get_config(config_file))
    ctrl.start_bot()


if __name__ == "__main__":
    main()
