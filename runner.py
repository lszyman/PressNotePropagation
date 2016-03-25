# -*- coding: utf-8 -*-
#!/usr/bin/env python

import os
import sys
from wordcount import WordCount
from dictionary_maker import DictionaryMaker
from pressnote import PressNote

if __name__ == '__main__':
	INPUT_DIR = 'geomedia'
	OUTPUT_DIR = 'outputs'
	
	if len(sys.argv) != 1:
		print "python runner.py"
	else:
		dictionary_maker = DictionaryMaker('en')
		dictionary_maker.parse(INPUT_DIR)
		dictionary_maker.dump(OUTPUT_DIR + os.sep + 'en_dictionary.txt')
		
		dictionary_maker = DictionaryMaker('es')
		dictionary_maker.parse(INPUT_DIR)
		dictionary_maker.dump(OUTPUT_DIR + os.sep + 'es_dictionary.txt')
		
		dictionary_maker = DictionaryMaker('fr')
		dictionary_maker.parse(INPUT_DIR)
		dictionary_maker.dump(OUTPUT_DIR + os.sep + 'fr_dictionary.txt')
