import random
import re

import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

from bot_config import get_bot_config, get_sec_key

BOT_CONFIG = get_bot_config()
x_input = []
y = []
for intent, data in BOT_CONFIG['intents'].items():
    for el in data['examples']:
        x_input.append(el)
        y.append(intent)
tfidf_vectorizer = TfidfVectorizer(analyzer='char_wb', ngram_range=(2, 4))
X = tfidf_vectorizer.fit_transform(x_input)
lin_svc = LinearSVC(penalty='l2')
lin_svc.fit(X, y)

def filter(text: str):
    text = text.lower()
    return ''.join(re.findall(r'\w|-| ', text))


def match(text, example):
    nltk.edit_distance(filter(text), filter(example))
    distance = nltk.edit_distance(filter(text), filter(example)) / len(example)
    if distance < 0.4:
        return True
    else:
        return False


def get_intent(text):
    for intent, data in BOT_CONFIG['intents'].items():
        for ask in data['examples']:
            if match(text, ask):
                return intent

def get_intent_predictive_model(text):

    return lin_svc.predict(tfidf_vectorizer.transform([text]))[0]



def get_answer_by_intent(intent):
    return random.choice(BOT_CONFIG['intents'][intent]['responses'])


def bot(text):
    # понять намерение
    intent = get_intent(text)

    if not intent:
        intent = get_intent_predictive_model(text)

    if intent:
        print(intent)
        return get_answer_by_intent(intent)

    # вернуть случайную фразу
    return random.choice(BOT_CONFIG['failure_phrases'])

def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Use request and receive answer')


def echo(update: Update, context: CallbackContext) -> None:
    """Answer to user  message"""
    update.message.reply_text(bot(update.message.text))


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(get_sec_key(), use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    # on noncommand i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()

