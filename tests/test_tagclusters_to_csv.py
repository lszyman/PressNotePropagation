# -*- coding: utf-8 -*-
#!/usr/bin/env python

import unittest
from tagclusters_to_csv import *

class TestTagClustersToCSV(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_clustering(self):
        main('tests/test_final_clusters.txt', 'tests/csv/')


if __name__ == '__main__':
    unittest.main()
