import os
import shutil
from unittest import TestCase

from nose.tools import assert_in, assert_true, assert_equals, assert_not_in

from hashtag_app import (get_file_names, add_words_from_file, read_file,
    get_freqs_docs_sentences_by_word, get_most_common_words)


__here__ = os.path.dirname(os.path.abspath(__file__))

test_str = """This is a test sentence string.
It contains the word sentence twice.
Here are some words repeated that should not be included in any hashtag:
I I I I I You You you You you We We We We we.
But here is a word that should be included:
I like pottery.
He likes pottery.
She likes pottery.
They love pottery."""

class TestHashtagApp(TestCase):
    def setUp(self):
        self.test_docs_dir = os.path.join(__here__, 'test_case')
        if not os.path.exists(self.test_docs_dir):
            os.makedirs(self.test_docs_dir)
        file_name = os.path.join(self.test_docs_dir, 'test_file.txt')
        with open(file_name, 'w') as f:
            f.write(test_str)

    def test_read_file(self):
        input_str = read_file('test_file.txt', self.test_docs_dir)
        assert_true(input_str.startswith('This is a test'))
        assert_true(input_str.endswith('They love pottery.'))

    def test_add_words_from_file(self):
        string_for_test = test_str.replace('\n', ' ')
        words_sentences_tuples = add_words_from_file(string_for_test)
        words = [w_s[0] for w_s in words_sentences_tuples]
        assert_in('hashtag', words)
        assert_in(('pottery', 'He likes pottery.'), words_sentences_tuples)

    def test_get_file_names(self):
        file_names = get_file_names(docs_dir=self.test_docs_dir)
        assert_in('test_file.txt', file_names)

    def test_get_freqs_docs_sentences_by_word(self):
        file_words_combined = {'test_file.txt': [
            ('test', 'This is a test sentence string.'), 
            ('sentence', 'This is a test sentence string.'), 
            ('string', 'This is a test sentence string.'), 
            ('word', 'It contains the word sentence twice.'), 
            ('sentence', 'It contains the word sentence twice.'), 
            ('words', 'Here are some words repeated that should not be included in any hashtag: I I I I I You You you You you We We We We we.'), 
            ('hashtag', 'Here are some words repeated that should not be included in any hashtag: I I I I I You You you You you We We We We we.'), 
            ('word', 'But here is a word that should be included: I like pottery.'), 
            ('pottery', 'But here is a word that should be included: I like pottery.'), 
            ('pottery', 'He likes pottery.'), 
            ('pottery', 'She likes pottery.'), 
            ('pottery', 'They love pottery.')]
        }
        freqs, docs, sentences = get_freqs_docs_sentences_by_word(file_words_combined)
        assert_equals(freqs['pottery'], 4)
        assert_equals(freqs['hashtag'], 1)
        for key in docs:
            assert_in('test_file.txt', docs[key])
        assert_in('He likes pottery.', sentences['pottery'])

    def test_get_most_common_words(self):
        freqs = {
            'quick': 10,
            'brown': 3,
            'fox': 15,
            'jumped': 20,
            'over': 100,
            'the': 6,
            'lazy': 4,
            'dog': 7
        }
        most_common_words = get_most_common_words(freqs, count=5)
        assert_in('over', most_common_words)
        assert_in('quick', most_common_words)
        assert_in('dog', most_common_words)
        assert_not_in('the', most_common_words)
        assert_not_in('lazy', most_common_words)

    def tearDown(self):
        shutil.rmtree(self.test_docs_dir)
