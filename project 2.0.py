import collections
import nltk
from nltk.util import ngrams
import random
import string
import time
start_time = time.time()

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
    line = line.replace('(', '')
    line = line.replace(')', '')
    return line

def parse_text(filename, n):
    ngram_list = []
    #кажется, мне сказали не называть переменные как "что-то_list", но иначе у меня так будет названа каждая вторая переменная и я запутаюсь (а ещё там есть одноименная функция)
    with open(filename, encoding='utf-8') as text:
        for line in text:
            #print(sentences) сделать что-то с прямой речью!!!
            #(что-то сделано в clean_punct)
            line = clean_punct(line)
            sentences = nltk.sent_tokenize(line)
            '''
            здесь был вопрос, что делать с многострочными предложениями
            Я думала об это и сама, но в всё-таки в файле txt, по-моему, редко бывает текст с переносами строк
            Возможно, я что-нибудь сделаю с этим, просто как дополнение к проекту (если пойму как)
            Но мне кажется, напрямую это моей программе не мешает, потому что в интернете довольно легко найти текст без переносов строк
            '''
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

def main():
    ngram_list = []
    #возможно, стоит сделать "хотите ли вы вообще что-то не по умолчанию" 
    n = int(input('Введите n, длину n-граммы: '))
    print('Вы хотите задать специальные тексты в качестве корпуса?')
    print('(в случае ответа \'нет\' будет использован корпус по умолчанию)')
    corpus_choice = input('Введите да/нет: ')
    if corpus_choice == 'нет':
        ngram_list.extend(parse_text('1.txt', n))
        ngram_list.extend(parse_text('2.txt', n))
    else:
        while True:
            filename = input('Введите имя файла или напишите "хватит": ')
            if filename == 'хватит':
                break
            else:
                ngram_list.extend(parse_text(filename, n))
    ngram_dict = collections.Counter(ngram_list)
    print('1 - сгенерировать новый текст')
    print('2 - получить предсказание следующего слова')
    function_choice = input('Введите 1/2: ')
    if function_choice == '1':
        text = ''
        sent_start = start_sentence(ngram_dict)
        num = int(input('Сколько предложений? '))
        #print('Этот раздел ещё не готов')
        for i in range(num):
            text += generate_sent(sent_start, ngram_dict, n)
        print(text)
    if function_choice == '2':
        line = input('Введите вашу фразу: ')
        line_list = nltk.word_tokenize(line)
        print('Сколько вариантов вы хотите получить?')
        variety = input('(Нажмите enter, чтобы выбрать параметр по умолчанию)')
        if variety != '':
            variety = int(variety)
            new = next_word(line_list, n, ngram_dict, variety)
            answer = 'Вот самые частотные варианты:'
            for word in new:
                answer = answer + ' ' + word + ','
            answer = answer[:-1] + '.'
            print (answer)
            #доделать красивую выдачу
        else:
            new = next_word(line_list, n, ngram_dict)
            print(new)
    #ngram_list = parse_text('4.txt', n)
    #ngram_dict = collections.Counter(ngram_list)
    #sent_start = start_sentence(ngram_dict)
    #print(sent_start)
    #print(generate_sent(sent_start, ngram_dict, n))
    #a = next_word('sadfgh waesrtdyu wersttf'.split(), n, ngram_dict, do_choice = True)
    #print(a)
    #if a == None:
        #print('А так можно')
    #print(clean_punct('Вот какая-то интересная - очень - "строка"'))

if __name__ == '__main__':
    main()
    print("--- %s seconds ---" % (time.time() - start_time))
