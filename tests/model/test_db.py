import fakeredis
import redis
import pytest

from slovodel_bot.model import db

def test_dictionary_existence_checkup(monkeypatch):
    mock_redis = fakeredis.FakeRedis(decode_responses=True)
    for letter in db.ALPHABET:
        mock_redis.sadd("some_other_dict:{}".format(letter), "0")

    def fake_the_redis(dummy1, dummy2, dummy3, dummy4):
        return mock_redis

    monkeypatch.setattr(redis, "Redis", fake_the_redis)

    db_config = db.Configuration("non_existent_dict", "localhost", 6379, 0, None)

    with pytest.raises(NameError):
        dictionary = db.Dictionary(db_config)



def test_word_existence_checkup(monkeypatch):
    mock_redis = fakeredis.FakeRedis(decode_responses=True)
    for letter in db.ALPHABET:
        mock_redis.sadd("dict1:{}".format(letter), "0")
    mock_redis.sadd("dict1:а", "абв")

    def fake_the_redis(dummy1, dummy2, dummy3, dummy4):
        return mock_redis

    monkeypatch.setattr(redis, "Redis", fake_the_redis)

    db_config = db.Configuration("dict1", "localhost", 6379, 0, None)

    dictionary = db.Dictionary(db_config)

    assert dictionary.word_exists("аб") == False
    assert dictionary.word_exists("абв") == True
    assert dictionary.word_exists("") == False
