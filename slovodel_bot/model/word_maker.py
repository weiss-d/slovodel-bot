"""
Generating words with Markov Chain and checking its existence in DB dictionary.
"""
from dataclasses import dataclass
from enum import Enum, unique
from pathlib import Path
from typing import Dict

import markovify

from slovodel_bot.model import db


@unique
class wordTypes(Enum):
    NOUN = "Существительное"
    ADJECTIVE = "Прилагательное"
    VERB = "Глагол"


@dataclass
class Configuration:
    """Module config."""
    chain_json_files: Dict[wordTypes, Path]
    db_config: db.Configuration


class Slovodel:
    """Class that is doing all the job, providing you with the freshiest and
    uniquest non-existent words."""

    def __init__(self, config: Configuration) -> None:
        self.dictionary = db.Dictionary(config.db_config)
        self.chains = {}
        for wtype in wordTypes:
            with config.chain_json_files[wtype].open() as json_file:
                self.chains[wtype] = markovify.Chain.from_json(json_file.read())

    def make_unique_word(self, word_type: wordTypes, attempts: int = 100) -> str:
        """Makes things happen.
        If you're increasing ammount of attempts, but the function still rises
        exceptions too often - try to increase the size of dictionary, that
        you're feeding to markovify.
        """

        for _ in range(attempts):
            word = "".join(self.chains[word_type].walk())
            if len(word) > 3 and not self.dictionary.word_exists(word):
                return word
        raise ValueError("Cannot produce unique word with given ammount of attempts.")
