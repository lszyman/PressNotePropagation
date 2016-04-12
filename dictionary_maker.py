# -*- coding: utf-8 -*-
#!/usr/bin/env python

import os
import sys
import operator
from pressnote import PressNote
from wordcount import WordCount


class DictionaryMaker:
	def __init__(self, language_code):
		self.language_codes = {'en': 'english', 'es': 'spanish', 'fr': 'french'}
		self.language_code = language_code
		self.wordcount = WordCount(self.language_codes[language_code])
		self.wordcount_dictionary = {}

	#parse only concrete language
	def parse_language(self, directory, max_parsed_pressnotes=None):  #max_parsed_pressnotes=None -> no limit
		n = 0
		for root, subFolders, files in os.walk(directory):
			for file in files:
				if root.split(os.sep)[-1].startswith(self.language_code) and file == 'rss.csv':
					print os.path.join(root, file)
					pressnote_list = PressNote.load(os.path.join(root, file))

					for pressnote in pressnote_list:
						self.wordcount.parse_text(pressnote.title, self.wordcount_dictionary)
						self.wordcount.parse_text(pressnote.text, self.wordcount_dictionary)
						n += 1
						if max_parsed_pressnotes is not None and n > max_parsed_pressnotes:
							break
		print "Parsed: " + str(n) + " press notes"

	#parse all languages with english version
	def parse(self, directory, max_parsed_pressnotes=None):  #max_parsed_pressnotes=None -> no limit
		n = 0
		for root, subFolders, files in os.walk(directory):
			for file in files:
				root_wanted = root.split(os.sep)[-1].startswith(self.language_code) #there is translation in rss2.csv
				if (root_wanted and file == 'rss.csv') or (not root_wanted and file == 'rss2.csv'):
					print os.path.join(root, file)
					pressnote_list = PressNote.load(os.path.join(root, file))

					for pressnote in pressnote_list:
						self.wordcount.parse_text(pressnote.title, self.wordcount_dictionary)
						self.wordcount.parse_text(pressnote.text, self.wordcount_dictionary)
						n += 1
						if max_parsed_pressnotes is not None and n > max_parsed_pressnotes:
							break
		print "Parsed: " + str(n) + " press notes"

	def dump(self, dictionary_name, dict_max_size=None):  #dict_max_size=None -> no limit
		sorted_wordcount = sorted(self.wordcount_dictionary.items(), key=operator.itemgetter(1), reverse=True)
		if(dict_max_size is not None):
			sorted_wordcount = sorted_wordcount[:dict_max_size]
		with open (dictionary_name, 'w') as f:
			keys = [item[0]+" "+str(item[1]) for item in sorted_wordcount]
			f.write('\n'.join(keys))
