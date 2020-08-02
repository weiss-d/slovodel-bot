import os
import pytest
from click.testing import CliRunner
import fakeredis
import redis
from slovodel_bot.utils import redis_upload_dict


def test_main(tmpdir, monkeypatch):
    dict_file = tmpdir.mkdir("sub").join("mydict.txt")

    dict_file.write(
        "Аба\n" + \
        "аБаба \n" + \
        "аб-ба\n" + \
        "бА\n" + \
        "бАба\n" + \
        "zвеве\n" + \
        "ве ве\n" + \
        "ве.\n"
    )

    mock_redis = fakeredis.FakeRedis(decode_responses=True)
    def fake_the_redis(dummy1, dummy2, dummy3, dummy4):
        return mock_redis

    monkeypatch.setattr(redis, "Redis", fake_the_redis)

    runner = CliRunner()
    result = runner.invoke(redis_upload_dict.main, [str(dict_file), "dict1"])

    assert "processed" in result.output
    assert result.exit_code == 0
    assert mock_redis.smembers('dict1:а') == {'аб-ба', 'аба'}
    assert mock_redis.smembers('dict1:б') == {'ба', 'баба'}
