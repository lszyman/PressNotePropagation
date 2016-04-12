# -*- coding: utf-8 -*-
#!/usr/bin/env python

import os
import sys
import operator
from pressnote import PressNote
from wordcount import WordCount


class BagOfWords:
	def __init__(self, dictionary_path, dir_notes, dict_max_size=None):
		self.bag_of_words = {}
		self.language_code = 'en'
		self.wordcount = WordCount('english')
		self.word_indexes = self.load_dictionary(dictionary_path, dict_max_size)
		self.create(dir_notes)

	@staticmethod
	def load_dictionary(dictionary_path, dict_max_size=None):  #dict_max_size=None -> no limit
		dict_indexes = {}
		index = 0
		with open (dictionary_path, 'r') as f:
			for line in f:
				dict_indexes[line.split(' ')[0]] = index
				index += 1
				if(dict_max_size is not None and index >= dict_max_size):
					break

		return dict_indexes
	
	#parse all languages with english version
	def create(self, dir_notes):
		pressnote_list = []
		for root, subFolders, files in os.walk(dir_notes):
			for file in files:
				root_wanted = root.split(os.sep)[-1].startswith(self.language_code) #there is translation in rss2.csv
				if (root_wanted and file == 'rss.csv') or (not root_wanted and file == 'rss2.csv'):
					print os.path.join(root, file)
					pressnote_list.append(PressNote.load_list(os.path.join(root, file))[0])

		for pressnote in pressnote_list:
			note_dictionary = {}
			self.wordcount.parse_text(pressnote.title, note_dictionary)
			self.wordcount.parse_text(pressnote.text, note_dictionary)
			word_vector = [0] * len(self.word_indexes)
			for key in note_dictionary:
				if key in self.word_indexes:
					idx = self.word_indexes[key]
					word_vector[idx] = note_dictionary[key]
			self.bag_of_words[pressnote] = word_vector

		print "Created bag of words\n"