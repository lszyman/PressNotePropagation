# -*- coding: utf-8 -*-
#!/usr/bin/env python

import os
import sys
import codecs
from translator import *

def parse_cluster_file(cluster_file_input, notes_csv_file, clusters_csv_file):
    tag = True
    current_cluster = 0
    for input_line in cluster_file_input:
        if tag:
            input_tokens = input_line.split(' ')
            current_cluster = input_tokens[0]
            input_tags = input_tokens[1].split(':')
            line = input_tokens[0] + '\t' + '\t'.join(input_tags)
            clusters_csv_file.write(line)
            tag = False
        elif input_line == '\n':
            tag = True
        else:
            input_tokens = input_line.split('\t')
            input_tokens[-1] = input_tokens[-1].replace('\n', '')
            input_tokens.append(current_cluster + '\n')
            line = '\t'.join(input_tokens)
            notes_csv_file.write(line)


def convert_cluster_to_csv(input_file, output_dir):
    with codecs.open(input_file, "r", "utf-8") as cluster_file_input:
        with codecs.open(output_dir + os.sep + "notes.csv", "wb", "utf-8") as notes_csv_file:
            with codecs.open(output_dir + os.sep + "clusters.csv", "wb", "utf-8") as clusters_csv_file:
                parse_cluster_file(cluster_file_input, notes_csv_file, clusters_csv_file)

def main(input_file, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    convert_cluster_to_csv(input_file, output_dir)

if __name__ == '__main__':
    if len(sys.argv) == 3:
        input_file = sys.argv[1]
        output_dir = sys.argv[2]
        main(input_file, output_dir)
    else:
        print "Usage:"
        print "  python -m tagclusters_to_csv [input_file] [output_dir]"
        print "  eg. python -m tagclusters_to_csv clustered_tags/file.txt dir_with_csv"
