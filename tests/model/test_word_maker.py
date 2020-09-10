from unittest.mock import patch

import markovify
import pytest

from slovodel_bot.model import word_maker
from slovodel_bot.model import db


@pytest.fixture
def slovodel_config(tmpdir):
    path = tmpdir.mkdir("sub")
    file_noun = path.join("noun.json")
    file_verb = path.join("verb.json")
    file_adjective = path.join("adjective.json")
    file_noun.write(markovify.Chain([["абв"]], 1).to_json())
    file_verb.write(markovify.Chain([["вгд"]], 1).to_json())
    file_adjective.write(markovify.Chain([["деж"]], 1).to_json())
    config = word_maker.Configuration(
        {
            word_maker.wordTypes.NOUN: file_noun,
            word_maker.wordTypes.VERB: file_verb,
            word_maker.wordTypes.ADJECTIVE: file_adjective,
        },
        db.Configuration("dummy", "dummy", 0, 0, None),
    )
    return config


@patch.object(db.Dictionary, "word_exists")
def test_word_generation_forgone_markovify(we_mock, slovodel_config):
    """The results of markovify.Chain.walk are forgone and reported
    by Dictionary as always unique."""
    we_mock.return_value = False

    slovodel = word_maker.Slovodel(slovodel_config)
    assert slovodel.make_unique_word(word_maker.wordTypes.NOUN) == "абв"
    assert slovodel.make_unique_word(word_maker.wordTypes.VERB) == "вгд"
    assert slovodel.make_unique_word(word_maker.wordTypes.ADJECTIVE) == "деж"


@patch.object(db.Dictionary, "word_exists")
def test_word_generation_not_unique(we_mock, slovodel_config):
    """The results of markovify.Chain.walk are forgone and reported
    by Dictionary as always NOT unique."""
    we_mock.return_value = True

    slovodel = word_maker.Slovodel(slovodel_config)

    for word_type in word_maker.wordTypes:
        with pytest.raises(ValueError) as error:
            slovodel.make_unique_word(word_type, attempts=1)
        assert (
            str(error.value)
            == "Cannot produce unique word with given ammount of attempts."
        )
