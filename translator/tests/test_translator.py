# -*- coding: utf-8 -*-
#!/usr/bin/env python

import unittest
from pressnote import *
from translator.translator import *

class TestTranslator(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_simple_translation(self):
        token = get_token()
        self.assertEquals(u'Dzi\u0119kuj\u0119', translate(u"thank you", token, 'en', 'pl'))
        self.assertEquals(u'The Nepal asked foreign relief teams not coming', translate(u"Le Népal demande aux équipes de secours étrangères de ne pas venir".encode('utf-8'), token, 'fr', 'en'))

    def test_find_dirs_without_translation(self):
        print find_dirs_without_translation('geomedia')

    def test_translate_one_file(self):
        dirs = find_dirs_without_translation('geomedia')
        first_dir = dirs[0]
        input_file = first_dir[0] + "/rss.csv"
        target_file = first_dir[0] + "/rss_en.csv"
        notes_list = PressNote.load_list(input_file)
        notes_list = translate_notes_list(notes_list, lang_in = first_dir[1])
        PressNote.serialize_list(notes_list, target_file)


if __name__ == '__main__':
    unittest.main()
