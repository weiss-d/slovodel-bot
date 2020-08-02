import os
from click.testing import CliRunner
from markovify import Chain
from slovodel_bot.utils import corpus_parser


def test_main(tmpdir):
    path = tmpdir.mkdir("sub")
    input_file = path.join("test_dict_1.txt")
    output_file = path.join("test_json_1.json")

    input_file.write("Аба\n" + "аБаба \n" + "аб-ба\n" + "zвеве\n" + "ве ве\n" + "ве.\n")

    corpus = [
        ["а", "ба"],
        ["а", "ба", "ба"],
        ["аб", "-", "ба"],
    ]
    chain = Chain(corpus, 1)

    runner = CliRunner()
    result = runner.invoke(corpus_parser.main, [str(input_file), str(output_file)])
    assert "processed" in result.output
    assert result.exit_code == 0
    with open(str(output_file), "r") as test_json_1:
        assert test_json_1.read() == chain.to_json()
