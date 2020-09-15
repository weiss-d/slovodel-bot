"""
Parse TOML config to a dataclass
"""
from pathlib import Path

import dacite
import toml

from slovodel_bot.controller import default_controller
from slovodel_bot.model.word_maker import wordTypes


def get_dataclass(file: Path) -> default_controller.Configuration:
    """Parse config file to controller.Configuration dataclass."""
    converters = {
        Path: Path,
        wordTypes: lambda x: wordTypes.__members__.get(x),
    }
    with open(file) as config:
        toml_config = toml.load(config)

    return dacite.from_dict(
        data_class=default_controller.Configuration,
        data=toml_config,
        config=dacite.Config(type_hooks=converters),
    )
