"""
CLI corpus parser for slovodel_bot.

Takes Russian dictionary text file with one line per wors as input
and produces a JSON file with syllable data, that could be fed to markovify library.

All symbols are ignored exept Russian letters and dashes.
All letters are converted to lowercase.
To get clean results each dictionary should contain only words of given type,
(nouns, adjectives or verbs).

Usage:
    $ python3 corpus_parser.py input_file output_file

Example:
    $ python3 corpus_parser.py \
        ~/data/corpus/rusdict_nouns.txt ../resources/rusdict_nouns.json
"""
import click
from markovify import Chain
from rusyll import rusyll


@click.command()
@click.argument("input_file", type=click.File("r"))
@click.argument("output_file", type=click.File("w+"))
def main(input_file, output_file):
    """Makes things happen."""
    corpus = []
    lines_processed = 0

    for line in input_file:
        lines_processed += 1
        try:
            corpus.append(rusyll.word_to_syllables_safe_wd(line.strip().lower()))
        except AssertionError:
            pass

    chain = Chain(corpus, 1)
    output_file.write(chain.to_json())

    print("{} lines processed. {} words added.".format(lines_processed, len(corpus)))


if __name__ == "__main__":
    main()
