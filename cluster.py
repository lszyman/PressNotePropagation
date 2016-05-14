# -*- coding: utf-8 -*-
#!/usr/bin/env python

import codecs
from pressnote import PressNote
from nltk.stem.snowball import SnowballStemmer

class Cluster:

	def __init__(self, id, tags):
		self.ID = id
		self.tags = tags
		self.stemm_tags = list(set(self.get_stemm_tags(tags)))
		self.pressnotes = []

	def __repr__(self):
		return self.to_string()

	def to_string(self):
		res = str(self.ID) + u" " + u':'.join(self.tags) + u"\n"
		for pressnote in self.pressnotes:
			res += pressnote.to_string() + u"\n"
		
		return res + u"\n"

	def get_stemm_tags(self, tags):
		stemm_tags = []
		current_stemmer = SnowballStemmer('english')
		for tag in self.tags:
			stemm_tags.append(current_stemmer.stem(tag.lower()))
		
		return stemm_tags

	def extend_cluster(self, cluster):
		self.stemm_tags = list(set(self.stemm_tags).intersection(cluster.stemm_tags))
		self.pressnotes.extend(cluster.pressnotes)
		current_stemmer = SnowballStemmer('english')
		new_tags = []
		for tag in self.tags:
			tag = tag.lower()
			stemm = current_stemmer.stem(tag)
			if stemm in self.stemm_tags:
				new_tags.append(tag)
		self.tags = list(set(new_tags))
	
	@staticmethod
	def load_list(filePath):
		clusters_list = []
		with codecs.open(filePath, "r", "utf-8") as file:
			lines = file.readlines()
			tag = True
			current_cluster = Cluster(-1, []);
			for line in lines:
				if tag:
					line = line.lower().split(' ')
					tags = line[1].strip().split(':')
					tag = False
					current_cluster = Cluster(line[0], tags)
				elif line != '\n':
					current_cluster.pressnotes.append(PressNote(line.split('\t')))
				if line == '\n':
					tag = True
					clusters_list.append(current_cluster)
		return clusters_list

	@staticmethod
	def serialize_list(clusters_list, target_file):
		with codecs.open(target_file, 'wb', "utf-8") as f:
			for cluster in clusters_list:
				f.write(cluster.to_string())
