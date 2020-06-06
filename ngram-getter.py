import collections
import nltk
from nltk.util import ngrams
import random
import string
import json

def clean_punct(line):
    line = line.replace('— ', '')
    line = line.replace('- ', '')
    line = line.replace('\"', '')
    line = line.replace('\'', '')
    line = line.replace(' (', ', ')
    line = line.replace('(', '')
    line = line.replace(')', '')
    line = line.replace('«', '')
    line = line.replace('»', '')
    return line

def parse_text(filename):
    sentences = []
    with open(filename, encoding='utf-8') as text:
        for line in text:
            line = clean_punct(line)
            sentences.extend(nltk.sent_tokenize(line))
    return sentences

def get_ngrams (line, n):
    line = '& ' + line
    tokens = nltk.word_tokenize(line)
    n_grams = list(ngrams(tokens, n))
    return n_grams

def start_sentence(ngram_dict):
    sent_start = []
    for ngram in ngram_dict:
        if ngram[0] == '&':
            for i in range(int(ngram_dict[ngram])):
                sent_start.append(ngram)
    return sent_start


def main():
    sentences = []
    sentences.extend(parse_text('hero.txt'))
    sentences.extend(parse_text('cheh.txt'))
    sentences.extend(parse_text('tol1.txt'))
    sentences.extend(parse_text('tol2.txt'))
    sentences.extend(parse_text('pres-nak.txt'))
    ngram_list = []
    for sentence in sentences:
        n_grams = get_ngrams(sentence, 3)
        ngram_list.extend(n_grams)
    #ngram_dict = collections.Counter(str(ngram) for ngram in ngram_list)
    with open('classics_3-ngram_list.json', 'w', encoding='utf-8') as file:
        json.dump(ngram_list, file, ensure_ascii=False)

if __name__ == '__main__':
    main()
