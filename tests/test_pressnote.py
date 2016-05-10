# -*- coding: utf-8 -*-
#!/usr/bin/env python

import unittest
import os
from pressnote import *

class TestPressNote(unittest.TestCase):
    serialization_target = "tests/rss_en.csv"

    def setUp(self):
        try:
            os.remove(self.serialization_target)
        except OSError:
            print "OSError"

    def tearDown(self):
        pass

    def test_serialization(self):
        notes_list = PressNote.load_list("tests/rss.csv")
        PressNote.serialize_list(notes_list, self.serialization_target)


if __name__ == '__main__':
    unittest.main()
