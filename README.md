# 'Slovodel' Telegram Bot
Making non-existent Russian words using Markov chains.
Бот, который придумывает несуществующие русские слова.

[ПОСМОТРЕТЬ В ДЕЙСТВИИ / TRY IT OUT](http://t.me/slovodel_bot)↗️

![]()
Посвящается Велимиру Хлебникову.

[TOC]

## Фармакология
Генерация псевдослов с помощью цепей Маркова на основе корпуса, полученного алгоритмическим делением на слоги слов из русского частотного словаря.

## Показания к применению

* **Экстремальный нейминг**
* **Острый переизбыток семантики**
* **Развлекательная недостаточность**

Ещё одна цель проекта - реализовать на практике:
* паттерн MVC на Python
* современный целостный подход к разработке на Python, описанный в [этой серии статей](https://cjolowicz.github.io/posts/hypermodern-python-01-setup/)↗️
* лучшие практики для работы с конфигурацией в Python, предложенные [здесь](https://www.notion.so/Best-Practices-for-Working-with-Configuration-in-Python-Applications-Preferred-Networks-Research--46a5dee5b1114c66a1eedd8624b67bad#24c930d67a8b452989164f25cc6322cf)↗️

Поэтому его структура немного сложнее обычного.

## Способ применения и дозы
### Установка и запуск
```bash
$ git clone https://github.com/weiss-d/slovodel-bot.git
$ cd slovodel-bot
$ pip install -r requirements.txt

# настроить конфигурацию как описано ниже
$ nano bot_config.toml

# загрузить словари в базу данных Redis
# если есть пароль, дописываем его в конце каждой команды
$ python slovodel_bot/utils/redis_upload_dict.py ../resources/dictionaries/nouns.txt SLOVODEL_DICT 127.0.0.1 6379 0
$ python slovodel_bot/utils/redis_upload_dict.py ../resources/dictionaries/adjectives.txt SLOVODEL_DICT 127.0.0.1 6379 0
$ python slovodel_bot/utils/redis_upload_dict.py ../resources/dictionaries/verbs.txt SLOVODEL_DICT 127.0.0.1 6379 0

# можно запускать!
$ python -m slovodel_bot
```
### Настройка
Дефолтный конфиг `bot_config.toml` лежит в корне репозитория.
В нём нужно прописать токен, полученный от Bot Father, а так же координаты Redis, если база запущена не локально - это делается в самой нижней секции конфига.

### Heroku
Помимо стандартных процедур по созданию приложения, описанных в документации Heroku, необходимо задать переменную окружения `HEROKU_APP_NAME`, содержащую имя вашего приложения из настоек:
```bash
$ heroku config:set HEROKU_APP_NAME=имя_вашего_приложения

```
Файлы `Procfile`, `requirements.txt` и `runtime.txt` содержат все необходимые инструкции и готовы к запуску. Если хотите сделать для Heroku отдельный файл конфигурации, то путь к нему нужно прописать в `Procfile` в качестве аргумента к `heroku.py`.

## TODO
- [ ] Добавить логи
- [ ] Добавить обработку исключений python-telegram-bot

## Вопросы / Предложения
По всем вопросам и предложениям не стесняясь открывайте issue.

## Состав
* [markovify](https://github.com/jsvine/markovify) - основа модели, отвечающая за формирование слов.
* [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot/) - самая популярная обёртка Telegram Bot API из кожи питона.
* [click](https://click.palletsprojects.com/) - библиотека для лёгкого и безболезненного создания CLI-интерфейсов в Python.
* [dacite](https://github.com/konradhalas/dacite) - библиотека для преобразования словарей в dataclass'ы.
* [rusyll](https://github.com/weiss-d/rusyll) - моя библиотека для алгоритмического деления русских слов на слоги.