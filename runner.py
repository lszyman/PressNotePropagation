# -*- coding: utf-8 -*-
#!/usr/bin/env python

import os
import sys
from wordcount import WordCount
from dictionary_maker import DictionaryMaker
from pressnote import PressNote
from bag_of_words import BagOfWords

if __name__ == '__main__':
	INPUT_DIR = 'geomedia' + os.sep + 'Geomedia_extract_AGENDA'
	OUTPUT_DIR = 'outputs'
	DICTIONARY_PATH = OUTPUT_DIR + os.sep + 'dictionary_aus.txt'
	CLUSTERS_PATH = OUTPUT_DIR + os.sep + 'clusters_aus.txt'
	
	if len(sys.argv) != 1:
		print "python runner.py"
	else:
		'''dictionary_maker = DictionaryMaker('en')
		dictionary_maker.parse(INPUT_DIR)
		dictionary_maker.dump(DICTIONARY_PATH)
		
		bag_of_words = BagOfWords('en', DICTIONARY_PATH, INPUT_DIR, 1000) #change None -> dictionary size
		bag_of_words.cluster(CLUSTERS_PATH);'''
		
		bag_of_words = BagOfWords('en', OUTPUT_DIR, INPUT_DIR, 1000) #change None -> dictionary size
		# bag_of_words = BagOfWords('es', OUTPUT_DIR, INPUT_DIR, 1000) #change None -> dictionary size
		# bag_of_words = BagOfWords('fr', OUTPUT_DIR, INPUT_DIR, 1000) #change None -> dictionary size
		