# -*- coding: utf-8 -*-
#!/usr/bin/env python

import os
import sys
import operator
from pressnote import PressNote
from wordcount import WordCount


class DictionaryMaker:
	def __init__(self, language):
		self.wordcount = WordCount(language)
		self.wordcount_dictionary = {}

	def parse(self, directory, max_parsed_pressnotes=None):  #max_parsed_pressnotes=None -> no limit
		n = 0
		for fn in os.listdir(directory):
			print directory + os.sep + fn
			pressnote_list = PressNote.load(directory + os.sep + fn)

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
