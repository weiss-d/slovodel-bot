from slovodel_bot.view import keyboard
from slovodel_bot.model import word_maker


def test_get_keyboard():
    kb_dict_referense = {
        "keyboard": [["Сущ.", "Глаг.", "Прил."]],
        "resize_keyboard": False,
        "one_time_keyboard": False,
        "selective": False,
    }

    assert keyboard.get_standard(word_maker.wordTypes).to_dict() == kb_dict_referense
