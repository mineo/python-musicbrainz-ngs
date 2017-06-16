# Tests for parsing of label queries

import unittest
import os
import sys
# Insert .. at the beginning of path so we use this version instead
# of something that's already been installed
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from test import _common

class GetLabelTest(unittest.TestCase):
    def setUp(self):
        self.datadir = os.path.join(os.path.dirname(__file__), "data", "label")

    def testLabelAliases(self):
        res = _common.open_and_parse_test_data(self.datadir, "022fe361-596c-43a0-8e22-bad712bb9548-aliases.xml")
        aliases = res.label.alias_list
        self.assertEqual(len(aliases.alias), 4)

        a0 = aliases.alias[0]
        self.assertEqual(a0.valueOf_, "EMI")
        self.assertEqual(a0.sort_name, "EMI")

        a1 = aliases.alias[1]
        self.assertEqual(a1.valueOf_, "EMI Records (UK)")
        self.assertEqual(a1.sort_name, "EMI Records (UK)")

        res = _common.open_and_parse_test_data(self.datadir, "e72fabf2-74a3-4444-a9a5-316296cbfc8d-aliases.xml")
        aliases = res.label.alias_list
        self.assertEqual(len(aliases.alias), 1)

        a0 = aliases.alias[0]
        self.assertEqual(a0.valueOf_, "Ki/oon Records Inc.")
        self.assertEqual(a0.sort_name, "Ki/oon Records Inc.")
        self.assertEqual(a0.begin_date, "2001-10")
        self.assertEqual(a0.end_date, "2012-04")
