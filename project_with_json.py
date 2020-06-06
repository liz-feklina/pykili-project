import collections
import nltk
from nltk.util import ngrams
import random
import string
import json
import os


files = ['romance_sent.json', 'kids_sent.json', 'detective_sent.json', 'classics_sent.json']

def get_ngrams (line, n):
    line = '& ' + line
    tokens = nltk.word_tokenize(line)
    n_grams = list(ngrams(tokens, n))
    return n_grams

def clean_punct(line):
    line = line.replace('— ', '')
    line = line.replace('- ', '')
    line = line.replace('\"', '')
    line = line.replace('\'', '')
    line = line.replace('(', ',')
    line = line.replace(')', ',')
    return line


def parse_text(filename, n):
    ngram_list = []
    if os.path.exists(filename):
        with open(filename, encoding='utf-8') as text:
            for line in text:
                line = clean_punct(line)
                sentences = nltk.sent_tokenize(line)
                for sentence in sentences:
                    n_grams = get_ngrams(sentence, n)
                    ngram_list.extend(n_grams)
    else:
        print('Этого файла не существует')
    return ngram_list


def parse_json(json_file, n):
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

def next_word(line_list, n, ngram_dict, variety = 1000, do_choice = False):
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
        words = []
        i = 0
        for ngram in sorted(variants, key=variants.get, reverse = True):
            if i < variety and not ngram[-1] in string.punctuation:
                words.append(ngram[-1])
                i += 1
            else:
                break
        if not words:
            return 'Мы не можем угадать следующее слово :('
        else:
            return words

def main():
    ngram_list = [] 
    while True:
        n = input('Введите n, длину n-граммы: ')
        if n.isdigit() and int(n) > 1:
            n = int(n)
            break
        else:
            print('Нужно ввести натуральное число больше 1! Попробуйте ещё раз')
    print('Выберите набор текстов.\n1 - любой\n2 - все\n3 - романы\n4 - детское\n5 - детектив\n6 - классика\n7 - свои файлы')
    print('Введите ваш выбор: ')
    while True:
        corpus_choice = input()
        if corpus_choice.isdigit() and 1 <= int(corpus_choice) <= 7:
            break
        else:
            print('Вы ввели что-то не то. Введите номер нужного варианта')
    if corpus_choice == '1':
        file = random.choice(files)
        ngram_list.extend(parse_json(file, n))
    if corpus_choice == '2':
        for file in files:
            ngram_list.extend(parse_json(file, n))
    if corpus_choice == '3':
        ngram_list.extend(parse_json("romance_sent.json", n))
    if corpus_choice == '4':
        ngram_list.extend(parse_json("kids_sent.json", n))
    if corpus_choice == '5':
        ngram_list.extend(parse_json("detective_sent.json", n))
    if corpus_choice == '6':
        ngram_list.extend(parse_json("classics_sent.json", n))
    if corpus_choice == '7':
        while True:
            filename = input('Введите имя файла или напишите "хватит": ')
            if filename == 'хватит':
                break
            else:
                ngram_list.extend(parse_text(filename, n))
    ngram_dict = collections.Counter(ngram_list)
    print('1 - сгенерировать новый текст\n2 - получить предсказание следующего слова')
    while True:
        function_choice = input('Введите 1/2: ')
        if function_choice == '1' or function_choice == '2':
            break
        else:
            print('Вы ввели что-то не то.')
    while True:
        if function_choice == '1':
            text = ''
            sent_start = start_sentence(ngram_dict)
            print('Сколько предложений?')
            while True:
                num = input()
                if num.isdigit() and int(num) > 0:
                    num = int(num)
                    break
                else:
                    print('Нужно ввести натуральное число! Попробуйте ещё раз')
            for i in range(num):
                text = text + ' ' + generate_sent(sent_start, ngram_dict, n)
            text = text[1:]
            print(text)
        if function_choice == '2':
            while True:
                line = input('Введите вашу фразу: ')
                line_list = nltk.word_tokenize(line)
                #print(line_list)
                if len(line) < n - 1:
                    print('Слишком короткая строка, она должна быть хотя бы длиной', n-1)
                elif line_list[-1] in string.punctuation:
                    print('Ваша фраза уже закончена, зачем её продолжать?')
                else:
                    break
            new = next_word(line_list, n, ngram_dict)
            if new == 'Мы не можем угадать следующее слово :(':
                print(new)
            else:
                num_of_var = len(next_word(line_list, n, ngram_dict))
                print('Найдено', num_of_var, 'вариантов.')
                variety = input('Сколько вариантов вы хотели бы получить? ')
                if variety.isdigit():
                    variety = int(variety)
                    new = next_word(line_list, n, ngram_dict, variety)
                    answer = 'Вот самые частотные варианты:'
                    for word in new:
                        if not word in string.punctuation:
                            answer = answer + ' \'' + word + '\','
                    answer = answer[:-1] + '.'
                    print(answer)
                else:
                    print('Выбран параметр по умолчанию')
                    answer = 'Вот самые частотные варианты:'
                    for word in new:
                        if not word in string.punctuation:
                            answer = answer + ' \'' + word + '\','
                    answer = answer[:-1] + '.'
                    print(answer)
        print('Ещё?')
        while True:
            repeat = input('Введите да/нет: ')
            if repeat == 'да' or repeat == 'нет':
                break
            else:
                print('Вы ввели что-то не то.')
        if repeat == 'нет':
            break

if __name__ == '__main__':
    main()
