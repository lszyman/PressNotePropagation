# -*- coding: utf-8 -*-
#!/usr/bin/env python

import os
import sys
from wordcount import WordCount
from dictionary_maker import DictionaryMaker
from pressnote import PressNote
from bag_of_words import BagOfWords

if __name__ == '__main__':
	INPUT_DIR = 'geomedia'
	OUTPUT_DIR = 'outputs'
	DICTIONARY_PATH = OUTPUT_DIR + os.sep + 'dictionary.txt'
	CLUSTERS_PATH = OUTPUT_DIR + os.sep + 'clusters.txt'
	
	if len(sys.argv) != 1:
		print "python runner.py"
	else:
		'''dictionary_maker = DictionaryMaker('en')
		dictionary_maker.parse(INPUT_DIR)
		dictionary_maker.dump(DICTIONARY_PATH)'''
		
		bag_of_words = BagOfWords(DICTIONARY_PATH, INPUT_DIR, 21373) #change None -> dictionary size
		bag_of_words.cluster(CLUSTERS_PATH);