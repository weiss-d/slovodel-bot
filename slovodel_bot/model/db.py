"""
Module to connect to Redis DB that contains a dictionary and check existence of a word.
"""
from dataclasses import dataclass
from typing import Union

import redis


ALPHABET = "абвгдежзиклмнопрстуфхцчшщэюя"


@dataclass
class Configuration:
    """Database configuration."""

    dictionary_name: str
    host: str = "localhost"
    port: int = 6379
    db_id: int = 0
    password: Union[str, None] = None


class Dictionary:
    """Dictionary of russian words based on Redis db."""

    def __init__(self, config: Configuration) -> None:
        """Instanciate Redis cliet, connect to the DB and validate contained there dictionary."""
        self.redis_client = redis.Redis(
            config.host, config.port, config.db_id, config.password
        )

        self.dictionary_name = config.dictionary_name
        for letter in ALPHABET:
            if not self.redis_client.exists(f"{self.dictionary_name}:{letter}"):
                raise NameError("Dictionary for letter '{}' is not found in database. Check your configuration or DB.".format(letter))

    def word_exists(self, word: str) -> bool:
        """Check existence of the word in dictionary."""
        if not word:
            return False
        return self.redis_client.sismember(f"{self.dictionary_name}:{word[0]}", word)
