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
		train_directory = INPUT_DIR;
		dictionary_name = OUTPUT_DIR + os.sep + 'dictionary.txt'
		
		dictionary_maker = DictionaryMaker('english')
		dictionary_maker.parse(train_directory)
		dictionary_maker.dump(dictionary_name)
