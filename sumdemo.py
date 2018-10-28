# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

from sumy.parsers.html import HtmlParser
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words


LANGUAGE = "english"
SENTENCES_COUNT = 2


if __name__ == "__main__":
    #url = "https://en.wikipedia.org/wiki/Python_(programming_language)"
    #parser = HtmlParser.from_url(url, Tokenizer(LANGUAGE))
    # or for plain text files
    parser = PlaintextParser.from_file("document.txt", Tokenizer(LANGUAGE))
    # parser = "The other day I went to the park and I meet my old friend, her name was Mary."
    # "I haven't seen her for years and I was very happy with this encounter. "
    # "We decided to go for a walk together and later that day we wanted to see a movie at 5pm. "
    # "However, an hour later, we meet another old friend of hers and it was also quite sudden. "
    # "So, we changed our plans once again and decided to go to the restaurant that was across the street."
    stemmer = Stemmer(LANGUAGE)

    summarizer = Summarizer(stemmer)
    summarizer.stop_words = get_stop_words(LANGUAGE)

    for sentence in summarizer(parser.document, SENTENCES_COUNT):
        print(sentence)