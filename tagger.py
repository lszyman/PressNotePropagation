# -*- coding: utf-8 -*-
#!/usr/bin/env python

import os
import sys
import operator
import codecs
from pressnote import PressNote
from wordcount import WordCount

def findTags(file_path, pressnotes, cluster_number, language_code):
	language_codes = {'en': 'english', 'es': 'spanish', 'fr': 'french'}
	wordcount = WordCount(language_codes[language_code])
	wordcount_dictionary = {}
	extras = {}
	
	for pressnote in pressnotes:
		wordcount.parse_text_extra(pressnote.title, wordcount_dictionary, extras)
		wordcount.parse_text_extra(pressnote.text, wordcount_dictionary, extras)
		
	sorted_wordcount = sorted(wordcount_dictionary.items(), key=operator.itemgetter(1), reverse=True)
	tags = []
	for item in sorted_wordcount: #item[0] to stemming
		sorted_extras = sorted(extras[item[0]].items(), key=operator.itemgetter(1), reverse=True)
		for item in sorted_extras:
			tags.append(item[0])
			break
		if len(tags) >= 10:
			break
	saveNotesToFile(file_path, pressnotes, cluster_number, tags)

def saveNotesToFile(file_path, pressnotes, cluster_number, tags):
	with codecs.open(file_path, 'a', "utf-8") as f:
		f.write(str(int(cluster_number)) + ' ' +  ":".join(tags) + u'\n')
		for pressnote in pressnotes:
			f.write(pressnote.to_string())
		f.write('\n')

if __name__ == '__main__':
	LANGUAGE_CODES = ['en']
	
	if len(sys.argv) != 1:
		print "python converter.py"
	else:
		for LANGUAGE_CODE in LANGUAGE_CODES:
			INPUT_DIR = 'outputs' + os.sep + 'Geomedia_extract_AGENDA' + os.sep + LANGUAGE_CODE
			OUTPUT_DIR = 'outputs' + os.sep + 'Geomedia_extract_AGENDA' + os.sep + LANGUAGE_CODE + '_tagged'
			
			for root, subFolders, files in os.walk(INPUT_DIR):
				for file in files:
					file_path = os.path.join(root, file)
					print file_path
					with codecs.open(file_path, "r", "utf-8") as f:
						cluster_number = f.readline()
						while cluster_number.strip() != '':
							pressnotes = []
							line = f.readline()
							while line.strip() != '':
								pressnotes.append(PressNote(line.split('\t')))
								line = f.readline()
							findTags(os.path.join(OUTPUT_DIR, file), pressnotes, cluster_number, LANGUAGE_CODE)	
							cluster_number = f.readline()
