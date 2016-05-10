# -*- coding: utf-8 -*-
#!/usr/bin/env python

import unittest
from pressnote import *
from translator.translator import *
from translator.translate_tags import *

class TestTranslateTags(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_simple_translation(self):
        main('translator/tests/tagged', 'translator/tests/tagged_translated')


if __name__ == '__main__':
    unittest.main()
