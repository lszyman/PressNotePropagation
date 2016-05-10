# -*- coding: utf-8 -*-
#!/usr/bin/env python

import os
import sys
from pressnote import PressNote


def saveNotesToFile(file_path, file_header, pressnotes):
		with open (file_path, 'w') as f:
			f.write(str(file_header))
			for pressnote in pressnotes:
				f.write(str(pressnote))


if __name__ == '__main__':
	INPUT_DIR = 'geomedia' + os.sep + 'Geomedia_extract_AGENDA' 
	
	if len(sys.argv) != 1:
		print "python converter.py"
	else:
		for root, subFolders, files in os.walk(INPUT_DIR):
			for file in files:
				if (file == 'rss_unique.csv') or (file == 'rss_en.csv'):
					header = ""
					with open(os.path.join(root, file), 'r') as content_file:
						header = content_file.readline();
					pressnote_list = PressNote.load_list(os.path.join(root, file))
					
					file_number = 1
					presnote_count = len(pressnote_list)
					offset = 0
					print "Count: " + str(presnote_count)
					
					if(presnote_count < 10000):
						print os.path.join(root, file)
						print "0 : " + str(presnote_count) + "  --- NO CONVERSION"
					else:
						while (presnote_count > 0):
							part_file_name = file.split(".")[0] + str(file_number) + ".csv"
							part_file_name2 = file.split(".")[0] + str(file_number+1) + ".csv"
							if(presnote_count > 19998):
								saveNotesToFile(os.path.join(root, part_file_name), header, pressnote_list[offset:offset+9999])
								print os.path.join(root, part_file_name)
								print str(offset) + ":" + str(offset+9999)
								presnote_count -= 9999
								offset += 9999
							else:
								saveNotesToFile(os.path.join(root, part_file_name), header, pressnote_list[offset:offset+presnote_count/2])
								saveNotesToFile(os.path.join(root, part_file_name2), header, pressnote_list[offset+presnote_count/2:])
								print os.path.join(root, part_file_name)
								print str(offset) + ":" + str(offset+presnote_count/2)
								print os.path.join(root, part_file_name2)
								print str(offset+presnote_count/2) + ":" + str(offset+presnote_count/2+len(pressnote_list[offset+presnote_count/2:]))
								presnote_count = 0
							file_number += 1
						
						os.remove(os.path.join(root, file))
