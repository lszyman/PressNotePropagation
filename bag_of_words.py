# -*- coding: utf-8 -*-
#!/usr/bin/env python

import os
import sys
import re
import operator
from pressnote import PressNote
from wordcount import WordCount
from dictionary_maker import DictionaryMaker
from sklearn.decomposition import TruncatedSVD
from sklearn.decomposition import RandomizedPCA
from sklearn.decomposition import PCA
from sklearn import datasets
from sklearn.cluster import AgglomerativeClustering

class BagOfWords:
	def __init__(self, language_code, dictionary_path, dir_notes, dict_max_size=None): #wersja klasterujaca wszystkie pliki
		self.bag_of_words = {}
		self.language_code = language_code
		language_codes = {'en': 'english', 'es': 'spanish', 'fr': 'french'}
		self.wordcount = WordCount(language_codes[language_code])
		self.word_indexes = self.load_dictionary(dictionary_path, dict_max_size)
		self.create(dir_notes)
		
	def __init__(self, language_code, output_dir, dir_notes, dict_max_size=None): #wersja klastrujaca notki z kazdego pliku z osobna
		self.bag_of_words = {}
		self.language_code = language_code
		language_codes = {'en': 'english', 'es': 'spanish', 'fr': 'french'}
		self.wordcount = WordCount(language_codes[language_code])
		self.dict_max_size = dict_max_size
		self.create2(dir_notes, output_dir)

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
				if (root_wanted and file == 'rss_unique.csv') or (not root_wanted and file == 'rss_en.csv'):
					print os.path.join(root, file)
					pressnote_list.extend(PressNote.load_list(os.path.join(root, file)))
		
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

		print "Created bag of words: " + str(len(self.bag_of_words)) + " x " + str(len(self.bag_of_words[pressnote_list[0]])) + "\n"
		
	#parse all files
	def create2(self, dir_notes, output_dir):
		pressnote_list = []
		for root, subFolders, files in os.walk(dir_notes):
			for file in files:
				self.bag_of_words = {}
				root_wanted = root.split(os.sep)[-1].startswith(self.language_code) #there is translation in rss2.csv
				pattern1 = re.compile(r'^rss_unique(\d)*\.csv$')
				pattern2 = re.compile(r'^rss_en(\d)*\.csv$')
				if (root_wanted and pattern1.match(file)) or (not root_wanted and pattern2.match(file)):
					pressnote_list = PressNote.load_list(os.path.join(root, file))

					dictionary_maker = DictionaryMaker(self.language_code)
					dictionary_maker.parse_language2(os.path.join(root, file))
					dictionary_maker.dump(output_dir + os.sep + 'temp_dictionary.txt')
					self.word_indexes = self.load_dictionary(output_dir + os.sep + 'temp_dictionary.txt', self.dict_max_size)
					
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

					print "Created bag of words: " + str(len(self.bag_of_words)) + " x " + str(len(self.bag_of_words[pressnote_list[0]])) + "\n"

					match_file = re.match(r'(rss_unique|rss_en)(\d)*\.csv', file)
					number = match_file.group(2)
					if number is None:
						number = ""
					self.cluster(output_dir + os.sep + root.split(os.sep)[-2] + os.sep + 'cluster_'+root.split(os.sep)[-1] + number + '.txt')
		
	def cluster(self, clusters_file_path):
		X = []
		Y = {}
		for key in self.bag_of_words:
			X.append(self.bag_of_words[key])
			# if(len(X) > 1000):	#usun
				# break

		# pca = PCA(n_components=min(len(X[0]), 5000))
		# pca.fit(X)
		# X = pca.transform(X)
		## pca = TruncatedSVD(n_components=100)
		## X = pca.fit_transform(X)
		# print "PCA - done"
		# print "Truncated bag of words of size: " + str(len(X)) + " x " + str(len(X[0])) + "\n"
		
		ward = AgglomerativeClustering(n_clusters=max(len(X)/30, 50), linkage='ward').fit(X)

		print "Clusters created: " + str(max(len(X)/30, 50))
		
		idx = 0
		for key in self.bag_of_words: # zachowana kolejnosc?!
			Y[key] = ward.labels_[idx]
			# if(len(Y) > 1000):	#usun
				# break
			idx+=1
		
		sorted_clusters = sorted(Y.items(), key=operator.itemgetter(1), reverse=False)
		
		cluster_number = 0;
		with open (clusters_file_path, 'w') as f:
			f.write(str(cluster_number) + "\n")
			for cluster in sorted_clusters:
				if cluster_number != cluster[1]:
					cluster_number = cluster[1]
					f.write("\n" + str(cluster_number) + "\n")
				f.write(str(cluster[0]))
		
		print "Clusters saved: " + clusters_file_path + "\n"