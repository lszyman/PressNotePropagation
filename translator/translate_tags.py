# -*- coding: utf-8 -*-
#!/usr/bin/env python

import os
import codecs
from translator import *

def translate_header(token, line, lang):
    line = line.split(' ')
    tags = line[1].split(':')
    translated_tags = []
    for tag in tags:
        translated_tags.append(translate(tag.encode('utf-8'), token, lang, 'en'))
    return_line = line[0] + " " + ":".join(translated_tags)
    return return_line

def translate_file(lang, input_file, output_file):
    token = get_token()
    with codecs.open(output_file, "wb", "utf-8") as cluster_file_output:
        with codecs.open(input_file, "r", "utf-8") as cluster_file_input:
            lines = cluster_file_input.readlines()
            tag = True
            for line in lines:
                if tag:
                    line = translate_header(token, line, lang)
                    tag = False
                if line == '\n':
                    tag = True
                cluster_file_output.write(line)

def translate_cluster(lang, cluster_file, input_dir, output_dir):
    input_file = input_dir + os.sep + cluster_file
    output_file = output_dir + os.sep + cluster_file
    translate_file(lang, input_file, output_file)

def translate_clusters(lang, files, input_dir, output_dir):
    for cluster_file in files:
        translate_cluster(lang, cluster_file, input_dir, output_dir)

def main(input_dir, output_dir):
    fr_clusters_input = input_dir + os.sep + 'fr_tagged'
    es_clusters_input = input_dir + os.sep + 'es_tagged'
    fr_clusters_output = output_dir + os.sep + 'fr_tagged'
    es_clusters_output = output_dir + os.sep + 'es_tagged'
    if not os.path.exists(fr_clusters_output):
        os.makedirs(fr_clusters_output)
    if not os.path.exists(es_clusters_output):
        os.makedirs(es_clusters_output)
    translate_clusters('fr', os.listdir(fr_clusters_input), fr_clusters_input, fr_clusters_output)
    translate_clusters('es', os.listdir(es_clusters_input), es_clusters_input, es_clusters_output)

if __name__ == '__main__':
    if len(sys.argv) == 3:
        input_dir = sys.argv[1]
        output_dir = sys.argv[2]
        main(input_dir, output_dir)
    else:
        print "Usage:"
        print "  python -m translator.translate_tags [input_dir] [output_dir]"
        print "  eg. python -m translator.translate_tags tags tags_translated"
