import collections
import nltk
import random

def text_parsing(filename, n):
    with open(filename, encoding='utf-8') as file:
        tok_list = []
        paragraphs = file.readlines()
        for line in paragraphs:
            sent_list = nltk.sent_tokenize(line)
            for sentence in sent_list:
                tokens_2 = nltk.word_tokenize(sentence)
                tokens = ['#start']
                tokens.extend(tokens_2)
                for i in range(len(tokens)- n + 1):
                    tok = ' '.join(tokens[i:(i + n)])
                    tok_list.append(tok)
    return tok_list

def text_generate(tok_list):
    text = ''
    starts = []
    for tok in tok_list:
        if tok.startswith('#start'):
            starts.append(tok)
    a = random.choice(starts)
    a = a.split()
    text += ' '.join(a[1:])
    while True:
        starts = []
        if a[-1] == '.' or a[-1] == '?' or a[-1] == '!':
            break
        start_tok = ' '.join(a[1:])
        start_tok = start_tok + ' '
        for tok in tok_list:
            if tok.startswith(start_tok):
                starts.append(tok)
        if len(starts) != 0:
            a = random.choice(starts)
            a = a.split()
            punct = ['.', ',', '!', '?', ':', ';']
            if a[-1] not in punct:
                text += ' '
            text += a[-1]
        else:
            text += '.'
            break
    return text

def main():
    tok_list = []
    n = int(input('Введите n, длину n-граммы: '))
    text = ''
    while True:
        filename = input('Введите имя файла или напишите "хватит": ')
        if filename == 'хватит':
            break
        else:
            tok_list.extend(text_parsing(filename, n))
    num = int(input('Сколько предложений? '))
    for i in range(num):
        text += text_generate(tok_list)
    print(text)

if __name__ == '__main__':
    main()
