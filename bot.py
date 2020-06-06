import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, ParseMode)
import collections
import nltk
nltk.download('punkt')
from nltk.util import ngrams
import random
import string
import json
#from functools import lru_cache

start_text = 'Это бот, который может сгенерировать фразу на основе разных жанров.\nЕсли ты не хочешь ничего настраивать, сразу тыкай /new. Или выбирай из предложенных вариантов то, что больше понравится :)'
TOKEN = ''
PORT = int(os.environ.get('PORT', '8443'))
HEROKU_APPNAME = 'text-generating'
genre = ['Детское', 'Роман', 'Детектив', 'Классика', 'Случайное', 'Все']
genre_files = ['kids_4-ngram_list.json', 'romance_4-ngram_list.json', 'detective_4-ngram_list.json', 'classics_4-ngram_list.json']
n = 4

def get_ngrams (line, n):
    line = '& ' + line
    tokens = nltk.word_tokenize(line)
    n_grams = list(ngrams(tokens, n))
    return n_grams

def parse_text(json_file, n):
    ngram_list = []
    with open(json_file, encoding='utf-8') as file:
        sentences = json.load(file)
    for sentence in sentences:
        n_grams = get_ngrams(sentence, n)
        ngram_list.extend(n_grams)
    return ngram_list

def start_sentence(ngram_dict):
    sent_start = []
    for ngram in ngram_dict:
        if ngram[0] == '&':
            for i in range(int(ngram_dict[ngram])):
                sent_start.append(ngram)
    return sent_start

def generate_sent(sent_start, ngram_dict, n):
    text = []
    start = random.choice(sent_start)
    text.extend(start)
    while True:
        if text[-1] == '.' or text[-1] == '?' or text[-1] == '!':
            break
        new = next_word(text, n, ngram_dict, do_choice = True)
        if new != 'Мы не можем угадать следующее слово :(':
            text.append(new)
            continue
        elif text[-1] in string.punctuation:
            text[-1] = '.'
            break
        else:
            text.append('.')
            break
    for i in range(len(text)- 1):
        if text[i] in string.punctuation or text[i] not in string.punctuation and text[i+1] not in string.punctuation:
            text[i] += ' '
    sentence = ''.join(text[1:])
    return sentence


def next_word(line_list, n, ngram_dict, variety = 3, do_choice = False):
    variants = {}
    line = line_list[-(n-1):]
    for ngram in ngram_dict:
        if ngram[:-1] == tuple(line):
            variants[ngram] = ngram_dict[ngram]
    if do_choice == True:
        choice_list = []
        for ngram in variants:
            for i in range(int(variants[ngram])):
                choice_list.append(ngram[-1])
        if choice_list:
            word = random.choice(choice_list)
            return word
        else:
            return 'Мы не можем угадать следующее слово :('
    else:
        word = []
        i = 0
        for ngram in sorted(variants, key=variants.get, reverse = True):
            if i < variety:
                word.append(ngram[-1])
                
                i += 1
            else:
                break
        if not word:
            return 'Мы не можем угадать следующее слово :('
        else:
            return word


def command_start(update, context):
    update.message.reply_text(
        start_text,
        reply_markup=ReplyKeyboardMarkup.from_column(genre)
    )


'''
def function_choice(update, context):
    if update.message.text == 'котик (новый текст)':
        update.message.reply_text(
            'А что будет дальше, пока непонятно\nА теперь надо выбрать жанр',
            reply_markup=ReplyKeyboardMarkup.from_column(genre))
        return 
    else:
        update.message.reply_text('Ну я же просил выбрать котика((( Будешь тыкать в пёсика - он скоро сдохнет.')
'''


def genre_choice(update, context):
    if update.message.text == 'Детское':
        update.message.reply_text(
            'Тыкни /newkids, и я сгенерирую фразу',
            reply_markup=ReplyKeyboardRemove())
    if update.message.text == 'Роман':
        update.message.reply_text(
            'Тыкни /newromance, и я сгенерирую фразу',
            reply_markup=ReplyKeyboardRemove())
    if update.message.text == 'Детектив':
        update.message.reply_text(
            'Тыкни /newdetective, и я сгенерирую фразу',
            reply_markup=ReplyKeyboardRemove())
    if update.message.text == 'Классика':
        update.message.reply_text(
            'Тыкни /newclassics, и я сгенерирую фразу',
            reply_markup=ReplyKeyboardRemove())
    if update.message.text == 'Случайное':
        update.message.reply_text(
            'Тыкни /newrandom, и я сгенерирую фразу',
            reply_markup=ReplyKeyboardRemove())


'''
@lru_cache(maxsize=7)
def parsing(json_file):
    ngram_list = parse_text(json_file, n)
    ngram_dict = collections.Counter(ngram_list)
    return ngram_dict
'''


def command_new(update, context):
    for file in genre_files:
        with open(file, encoding='utf-8') as file:
            ngram_list = json.load(file)
    ngram_dict = collections.Counter(tuple(ngram) for ngram in ngram_list)
    sent_start = start_sentence(ngram_dict)
    new_text = generate_sent(sent_start, ngram_dict, n)
    update.message.reply_text(
        new_text
    )


def command_newkids(update, context):
    with open('kids_4-ngram_list.json', encoding='utf-8') as file:
        ngram_list = json.load(file)
    ngram_dict = collections.Counter(tuple(ngram) for ngram in ngram_list)
    sent_start = start_sentence(ngram_dict)
    new_text = generate_sent(sent_start, ngram_dict, n)
    update.message.reply_text(
        new_text
    )


def command_newromance(update, context):
    with open('romance_4-ngram_list.json', encoding='utf-8') as file:
        ngram_list = json.load(file)
    ngram_dict = collections.Counter(tuple(ngram) for ngram in ngram_list)
    sent_start = start_sentence(ngram_dict)
    new_text = generate_sent(sent_start, ngram_dict, n)
    update.message.reply_text(
        new_text
    )

def command_newdetective(update, context):
    with open('detective_4-ngram_list.json', encoding='utf-8') as file:
        ngram_list = json.load(file)
    ngram_dict = collections.Counter(tuple(ngram) for ngram in ngram_list)
    sent_start = start_sentence(ngram_dict)
    new_text = generate_sent(sent_start, ngram_dict, n)
    update.message.reply_text(
        new_text
    )


def command_newclassics(update, context):
    with open('classics_4-ngram_list.json', encoding='utf-8') as file:
        ngram_list = json.load(file)
    ngram_dict = collections.Counter(tuple(ngram) for ngram in ngram_list)
    sent_start = start_sentence(ngram_dict)
    new_text = generate_sent(sent_start, ngram_dict, n)
    update.message.reply_text(
        new_text
    )


def command_newrandom(update, context):
    file = random.choice(genre_files)
    with open(file, encoding='utf-8') as file:
        ngram_list = json.load(file)
    ngram_dict = collections.Counter(tuple(ngram) for ngram in ngram_list)
    sent_start = start_sentence(ngram_dict)
    new_text = generate_sent(sent_start, ngram_dict, n)
    update.message.reply_text(
        new_text
    )


def answer(update, context):
    '''
    filename = update.message.document
    with open(filename, encoding='utf-8') as text:
        words = text.read()
        update.message.reply_text(words)
    '''
    update.message.reply_text('Оно тебя слышит, но делать ничего не будет')


def main():
    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', command_start))

    #dp.add_handler(MessageHandler(Filters.text(functions), function_choice))

    dp.add_handler(MessageHandler(Filters.text(genre), genre_choice))

    dp.add_handler(CommandHandler('new', command_new))

    dp.add_handler(CommandHandler('newkids', command_newkids))

    dp.add_handler(CommandHandler('newromance', command_newromance))

    dp.add_handler(CommandHandler('newdetective', command_newdetective))

    dp.add_handler(CommandHandler('newclassics', command_newclassics))

    dp.add_handler(CommandHandler('newrandom', command_newrandom))    
    
    dp.add_handler(MessageHandler(Filters.document.mime_type("text/plain"), answer))

    updater.start_webhook(listen='0.0.0.0', port=PORT, url_path=TOKEN)
    updater.bot.set_webhook(f'https://{HEROKU_APPNAME}.herokuapp.com/{TOKEN}')
    
    updater.idle()


if __name__ == '__main__':
    main()
