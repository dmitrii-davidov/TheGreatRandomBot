# coding: utf-8

import argparse
import os

import random
import re
import sys
import telepot
import time


# try:
#     import ptvsd
#     ptvsd.enable_attach('my_secret', address=('0.0.0.0', 3010))
#     ptvsd.wait_for_attach()
#     time.sleep(1)
# except:
#     pass


class Question:

    _SEPARATORS = [
        ('or', 'en'),
        ('или', 'ru'),
    ]
    _ANSWER_TEMPLATES = {
        'en': 'The Great Random has chosen {variant}! Take it for granted.',
        'ru': 'Великий Рандом выбрал {variant}! Прими это как должное.',
    }

    def __init__(self, variants, locale):
        self.variants = variants
        self.locale = locale

    @classmethod
    def analyze(cls, text) -> 'Question':
        for s, l in cls._SEPARATORS:
            if re.search(r'\W{}\W'.format(s), text):
                print('Found {} separator -> {} locale.'.format(s, l))
                return cls(
                    variants=[cls.normalize_variant_text(t) for t in text.split(s)],
                    locale=l,
                )

    @staticmethod
    def normalize_variant_text(text):
        text = text.strip().lower()
        if text[-1] in ',.?':
            text = text[:-1]
        return text

    def answer(self) -> str:
        return self._ANSWER_TEMPLATES[self.locale].format(
            variant=random.choice(self.variants),
        )


class TheGreatRandomBot(telepot.Bot):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def on_chat_message(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        text = msg['text']
        print('Message: {} {} id={} text="{}"'.format(content_type, chat_type, chat_id, text))

        question = Question.analyze(text)
        if question:
            self.sendMessage(chat_id, question.answer())
        else:
            self.sendMessage(chat_id, 'Спрашивай!')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='The Great Random Bot')
    parser.add_argument('--token', action='store')
    args = parser.parse_args()

    token = args.token or os.environ['TELEPOT_TOKEN']

    bot = TheGreatRandomBot(token)
    bot.message_loop()

    print('Listening ...')
    while True:
        sys.stdout.flush()
        time.sleep(10)
