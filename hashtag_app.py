import io
from collections import defaultdict
from multiprocessing import Pool
import os
import operator

from flask import Flask, render_template
from nltk import sent_tokenize, word_tokenize, pos_tag

from config import NLTK_DATA_DIR, DOCS_DIR

app = Flask(__name__)
os.environ['NLTK_DATA'] = NLTK_DATA_DIR


def read_file(file_name, docs_dir=DOCS_DIR):
    path = os.path.join(docs_dir, file_name)
    with io.open(path, encoding='utf-8') as f:
        text_from_file = ' '.join(f.read().splitlines())
    return text_from_file


def add_words_from_file(text_from_file):
    words_from_file = []
    for sentence in sent_tokenize(text_from_file):
        valid_words = [word[0] for word in pos_tag(word_tokenize(sentence)) 
            if word[1].startswith('NN')]
        for word in valid_words:
            lower_case_word = word.lower()
            words_from_file.append((lower_case_word, sentence))
    return words_from_file


def get_file_names(docs_dir=DOCS_DIR):
    return os.listdir(docs_dir)


def file_handler(file_name):
    text_from_file = read_file(file_name)
    words_from_file = add_words_from_file(text_from_file)
    words_from_file = (file_name, words_from_file)
    return words_from_file


def get_words_by_file():
    file_names = get_file_names()
    pool = Pool()
    words_from_files = pool.map(file_handler, file_names)
    file_words_combined = {f_words[0]: f_words[1] for f_words in words_from_files}
    return file_words_combined


def get_freqs_docs_sentences_by_word(file_words_combined):
    freqs = defaultdict(int)
    docs = defaultdict(set)
    sentences = defaultdict(list)
    for file_name in file_words_combined:
        word_sentence_list = file_words_combined[file_name]
        for (word, sentence) in word_sentence_list:
            freqs[word] += 1
            docs[word].add(file_name)
            sentences[word].append(sentence)
    return freqs, docs, sentences


def get_most_common_words(freqs, count=25):
    """Returns the 25 most common words by default"""
    sorted_by_common = sorted(freqs.items(), key=operator.itemgetter(1), reverse=True)
    most_common_words = [tpl[0] for tpl in sorted_by_common[:count]]
    return most_common_words


def get_data_for_table():
    file_words_combined = get_words_by_file()
    freqs, docs, sentences = get_freqs_docs_sentences_by_word(file_words_combined)
    most_common_words = get_most_common_words(freqs)
    for word in most_common_words:
        yield (word, docs[word], sentences[word])


@app.route("/", methods=['GET'])
def index():
    file_names = get_file_names()
    return render_template("index.html", files=file_names)


@app.route("/hashtags", methods=['GET'])
def hashtags():
    data_for_table = list(get_data_for_table())
    return render_template("hashtags.html", data=data_for_table)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
