# -*- coding: utf-8 -*-
#!/usr/bin/env python

import codecs

class PressNote:
	def __init__(self, id, feed, time, title, text):
		self.ID = id
		self.feed = feed
		self.time = time
		self.title = title
		self.text = text

	def __init__(self, pressNoteSplitted):
		self.ID = pressNoteSplitted[0]
		self.feed = pressNoteSplitted[1]
		self.time = pressNoteSplitted[2]
		self.title = pressNoteSplitted[3]
		self.text = pressNoteSplitted[4]
	
	def __repr__(self):
		return self.to_string()
		
	def to_list(self):
		return [self.ID, self.feed, self.time, self.title, self.text]
	
	def to_string(self):
		return u'\t'.join(self.to_list())
	
	@staticmethod
	def load_list(filePath):
		with codecs.open(filePath, "r", "utf-8") as csv_file:
			listOfNotes = [PressNote(line.split('\t')) for line in csv_file]
			return listOfNotes[1:]	#remove file header
