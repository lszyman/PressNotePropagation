# -*- coding: utf-8 -*-
#!/usr/bin/env python

import os
import re
from nltk import download
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer

class WordCount:
	def __init__(self, language):
		self.stopwords = self.load_stopwords(language)
		self.parse_regexp = re.compile(r"([0-9]*[a-zA-Z][a-zA-Z0-9]+)", re.DOTALL)
		self.current_stemmer = SnowballStemmer(language)

	@staticmethod
	def load_stopwords(language):
		stoplist = []
		if language == 'english':
			with open('geomedia'+ os.sep +'en_stoplist.txt') as f:
				stoplist = [line.rstrip() for line in f]
		else:
			download('stopwords')
			stoplist = stopwords.words(language)

		return stoplist

	def parse_text(self, text, wordcount_dictionary=None):
		"""
		>>> wordcount = WordCount() #doctest: +ELLIPSIS
		[nltk_data] ...
		>>> wordcount.parse_text("a1a ma kota")
		{'ma': 1, 'a1a': 1, 'kota': 1}
		>>> wordcount.parse_text("a1a ma kota", {'a1a': 2, 'kota': 1})
		{'ma': 1, 'a1a': 3, 'kota': 2}
		"""
		if wordcount_dictionary is None:
			wordcount_dictionary = {}
		words = self.parse_regexp.findall(text)
		for word in words:
			new_word = self.current_stemmer.stem(word.lower())
			if word not in self.stopwords and new_word not in self.stopwords:
				if new_word in wordcount_dictionary:
					wordcount_dictionary[new_word] += 1
				else:
					wordcount_dictionary[new_word] = 1
		return wordcount_dictionary
