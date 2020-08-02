"""
Upload a dictionary from file to Redis DB.

File format:
    * one word per line;
    * all words with symbols other than Russian letters and dashes are ignored;
    * all letters are transformed to lowercase.

Usage:
    $ python3 redis_upload_dict.py FILE DICT_NAME [DB_ADDRESS] [PORT] [DB_ID] [PASSWORD]

    Defaults: DB_ADDRESS=localhost, PORT=6379, PASSWORD=None

Example:
    $ pytho3 redis_upload_dict.py mydict.txt dict1
"""
import re

import redis
import click


@click.command()
@click.argument("input_file", type=click.File("r"))
@click.argument("dict_name")
@click.argument("host", default="localhost")
@click.argument("port", default="6379")
@click.argument("db_id", default=0)
@click.argument("password", default="")
def main(input_file, dict_name, host, port, db_id, password):
    """Makes things happen."""
    lines_processed = 0
    words_added = 0
    rc = redis.Redis(host, port, db_id, password)
    with rc.pipeline() as pipe:
        for line in input_file:
            lines_processed += 1
            if re.match(r"\A(?!-)(?!.*-\Z)\A[а-яА-ЯёЁ-]*$", line):
                clean_line = line.strip().lower()
                pipe.sadd("{}:{}".format(dict_name, clean_line[0]), clean_line)
                words_added += 1
        pipe.execute()
    print("{} lines processed. {} words addes".format(lines_processed, words_added))
