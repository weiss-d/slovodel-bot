from slovodel_bot.view import keyboard
from slovodel_bot.model import word_maker


def test_get_keyboard():
    kb_dict_referense = {
        "keyboard": [["Существительное", "Прилагательное", "Глагол"]],
        "resize_keyboard": True,
        "one_time_keyboard": False,
        "selective": False,
    }

    assert keyboard.get_standard(word_maker.wordTypes).to_dict() == kb_dict_referense
