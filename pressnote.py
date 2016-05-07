# -*- coding: utf-8 -*-
#!/usr/bin/env python

import unicodecsv as csv

class PressNote:
    def __init__(self, id, feed, time, title, text):
        self.ID = id
        self.feed = feed
        self.time = time
        self.title = title
        self.text = text

    def __init__(self, pressNoteSplitted):
        self.ID = pressNoteSplitted[0].replace("\"", '').strip()
        self.feed = pressNoteSplitted[1].replace("\"", '').strip()
        self.time = pressNoteSplitted[2].replace("\"", '').strip()
        self.title = pressNoteSplitted[3].replace("\"", '').strip()
        self.text = pressNoteSplitted[4].replace("\"", '').strip()

    def __repr__(self):
        return "-TITLE:" + self.title + "\n" + "-TEXT:" + self.text + "\n\n"

    def to_list(self):
        return [int(self.ID), self.feed, self.time, self.title, self.text]

    @staticmethod
    def load_list(filePath):
        with open(filePath, "r") as csv_file:
            listOfNotes = [PressNote(line.split('\t')) for line in csv_file]
            return listOfNotes[1:]	#remove file header

    @staticmethod
    def serialize_list(notes_list, target_file):
        with open(target_file, 'wb') as f:
            csv_writer = csv.writer(f, delimiter='\t', quoting=csv.QUOTE_NONNUMERIC, quotechar='\"')
            csv_writer.writerow(["ID", "feed", "time", "text1", "text2"])
            for note in notes_list:
                csv_writer.writerow(note.to_list())

