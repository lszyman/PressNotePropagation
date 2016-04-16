# -*- coding: utf-8 -*-
#!/usr/bin/env python

import os
import sys
import operator
from pressnote import PressNote
from wordcount import WordCount
from sklearn.decomposition import TruncatedSVD
from sklearn.decomposition import RandomizedPCA
from sklearn import datasets
from sklearn.cluster import AgglomerativeClustering

gcv_mode="eigen"

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
		self.pressnote_list = []
		for root, subFolders, files in os.walk(dir_notes):
			for file in files:
				root_wanted = root.split(os.sep)[-1].startswith(self.language_code) #there is translation in rss2.csv
				if (root_wanted and file == 'rss.csv') or (not root_wanted and file == 'rss2.csv'):
					print os.path.join(root, file)
					self.pressnote_list.extend(PressNote.load_list(os.path.join(root, file)))

		for pressnote in self.pressnote_list:
			note_dictionary = {}
			self.wordcount.parse_text(pressnote.title, note_dictionary)
			self.wordcount.parse_text(pressnote.text, note_dictionary)
			word_vector = [0] * len(self.word_indexes)
			for key in note_dictionary:
				if key in self.word_indexes:
					idx = self.word_indexes[key]
					word_vector[idx] = note_dictionary[key]
			self.bag_of_words[pressnote] = word_vector

		print "Created bag of words: " + str(len(self.bag_of_words)) + " x " + str(len(self.bag_of_words[self.pressnote_list[0]])) + "\n"
		
	def cluster(self, clusters_file_name):
		X = []
		Y = {}
		for key in self.bag_of_words:
			X.append(self.bag_of_words[key])
			if(len(X) > 1000):	#usun
				break

		# pca = decomposition.PCA(n_components=6000)
		# pca.fit(X)
		# X = pca.transform(X)
		# pca = TruncatedSVD(n_components=100)
		# X = pca.fit_transform(X)
		# print "PCA - done"
		# print "Truncated bag of words of size: " + str(len(X)) + " x " + str(len(X[0])) + "\n"
		
		ward = AgglomerativeClustering(n_clusters=50, linkage='ward').fit(X)

		print "Clusters created\n"
		
		idx = 0
		for key in self.bag_of_words: # zachowana kolejnosc?!
			Y[key] = ward.labels_[idx]
			if(len(Y) > 1000):	#usun
				break
			idx+=1
		
		sorted_clusters = sorted(Y.items(), key=operator.itemgetter(1), reverse=False)
		
		cluster_number = 0;
		with open (clusters_file_name, 'w') as f:
			f.write(str(cluster_number) + "\n")
			for cluster in sorted_clusters:
				if cluster_number != cluster[1]:
					cluster_number = cluster[1]
					f.write("\n" + str(cluster_number) + "\n")
				f.write(str(cluster[0]))
		
		print "Clusters saved\n"