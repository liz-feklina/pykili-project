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

def main():
    sentences = []
    sentences.extend(parse_text('hero.txt'))
    sentences.extend(parse_text('cheh.txt'))
    sentences.extend(parse_text('tol1.txt'))
    sentences.extend(parse_text('tol2.txt'))
    sentences.extend(parse_text('pres-nak.txt'))
    with open('classics_sent.json', 'w', encoding='utf-8') as file:
        json.dump(sentences, file, ensure_ascii=False)

if __name__ == '__main__':
    main()
