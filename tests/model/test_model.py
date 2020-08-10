from unittest.mock import patch
import pytest

import markovify

from slovodel_bot.model import model
import slovodel_bot.model.db as db


@pytest.fixture
def slovodel_config(tmpdir):
    path = tmpdir.mkdir("sub")
    file_noun = path.join("noun.json")
    file_verb = path.join("verb.json")
    file_adjective = path.join("adjective.json")
    file_noun.write(markovify.Chain([["абв"]], 1).to_json())
    file_verb.write(markovify.Chain([["вгд"]], 1).to_json())
    file_adjective.write(markovify.Chain([["деж"]], 1).to_json())
    config = model.Configuration(
        {
            model.wordTypes.NOUN: file_noun,
            model.wordTypes.VERB: file_verb,
            model.wordTypes.ADJECTIVE: file_adjective,
        },
        db.Configuration("dummy", "dummy", 0, 0, None),
    )
    return config


@patch.object(db.Dictionary, "word_exists")
def test_word_generation_forgone_markovify(we_mock, slovodel_config):
    """The results of markovify.Chain.walk are forgone and reported
    by Dictionary as always unique."""
    we_mock.return_value = False

    slovodel = model.Slovodel(slovodel_config)
    assert slovodel.make_unique_word(model.wordTypes.NOUN) == "абв"
    assert slovodel.make_unique_word(model.wordTypes.VERB) == "вгд"
    assert slovodel.make_unique_word(model.wordTypes.ADJECTIVE) == "деж"


@patch.object(db.Dictionary, "word_exists")
def test_word_generation_not_unique(we_mock, slovodel_config):
    """The results of markovify.Chain.walk are forgone and reported
    by Dictionary as always NOT unique."""
    we_mock.return_value = True

    slovodel = model.Slovodel(slovodel_config)

    for word_type in model.wordTypes:
        with pytest.raises(ValueError) as error:
            slovodel.make_unique_word(word_type, attempts=1)
        assert (
            str(error.value)
            == "Cannot produce unique word with given ammount of attempts."
        )
