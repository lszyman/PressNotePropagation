# -*- coding: utf-8 -*-
#!/usr/bin/env python

import os
import sys
import operator
import codecs
from wordcount import WordCount
from cluster import Cluster
from bag_of_words import BagOfWords
from sklearn.cluster import AgglomerativeClustering


def dump(dictionary_name, sorted_wordcount):  #dict_max_size=None -> no limit
	with codecs.open(dictionary_name, 'w', "utf-8") as f:
		keys = [item[0]+" "+str(item[1]) for item in sorted_wordcount]
		f.write('\n'.join(keys))
	
def set_clusters_new_id(clusters_list):
	id = 0
	for cluster in clusters_list:
		cluster.ID = id
		id += 1

def get_sorted_intersected_tags(clusters_list, min_intersection_size):
	intersected_tags = {}
	for i in range(len(clusters_list)):
		for j in range(i+1, len(clusters_list)):
			intersection_set = set(clusters_list[i].stemm_tags).intersection(clusters_list[j].stemm_tags)
			if len(intersection_set) >= min_intersection_size:
				key = u':'.join(intersection_set)
				if key in intersected_tags:
					intersected_tags[key] += 1
				else:
					intersected_tags[key] = 1
			if i % 1000 == 0 and j == i+1:
				print str(i) + "/" + str(len(clusters_list))

	sorted_intersected_tag = sorted(intersected_tags.items(), key=operator.itemgetter(1), reverse=True)
	dump('outputs' + os.sep + 'intersections.txt', sorted_intersected_tag)
	return sorted_intersected_tag

def merge_clusters(clusters_list, min_intersection_size, OUTPUT_PATH):
	sorted_intersected_tag = get_sorted_intersected_tags(clusters_list, min_intersection_size)
	
	print 'Size before merge: ' + str(len(clusters_list))
	for item in sorted_intersected_tag:
		merged_cluster = None
		for cluster in clusters_list:
			if(set(item[0].split(":")).issubset(set(cluster.stemm_tags))):
				if(merged_cluster == None):
					merged_cluster = cluster
				else:
					print '- merged clusters: ' + str(merged_cluster.ID) + ' and ' + str(cluster.ID)
					merged_cluster.extend_cluster(cluster)
					clusters_list.remove(cluster)
	
	print 'Size after merge: ' + str(len(clusters_list))
	Cluster.serialize_list(clusters_list, OUTPUT_PATH)
	
if __name__ == '__main__':
	if len(sys.argv) != 2:
		print "python converter.py [min_intersection_tag_size]"
	else:
		min_intersection_size = int(sys.argv[1])
		INPUT_DIR = 'outputs' + os.sep + 'Geomedia_extract_AGENDA' + os.sep + 'merged'
		OUTPUT_PATH = 'outputs' + os.sep + 'final_clusters.txt'
		
		clusters_list = []
		for root, subFolders, files in os.walk(INPUT_DIR):
			for file in files:
				clusters_list.extend(Cluster.load_list(os.path.join(root, file)))
		
		# set_clusters_new_id(clusters_list)
		# Cluster.serialize_list(clusters_list, OUTPUT_PATH)  dump clusters before merge
		print 'Clusters loaded'
		
		merge_clusters(clusters_list, min_intersection_size, OUTPUT_PATH)