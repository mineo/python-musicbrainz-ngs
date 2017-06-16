# Tests for parsing of release queries

import unittest
import os
import sys
# Insert .. at the beginning of path so we use this version instead
# of something that's already been installed
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from test import _common


class GetReleaseGroupTest(unittest.TestCase):
    def setUp(self):
        self.datadir = os.path.join(os.path.dirname(__file__), "data",
                "release-group")

    def testTypesExist(self):
        res = _common.open_and_parse_test_data(self.datadir,
                          "f52bc6a1-c848-49e6-85de-f8f53459a624.xml")
        rg = res.release_group
        self.assertTrue(hasattr(rg, "type_"))
        self.assertTrue(hasattr(rg, "primary_type"))
        self.assertTrue(hasattr(rg, "secondary_type_list"))

    def testTypesResult(self):
        res = _common.open_and_parse_test_data(self.datadir,
                          "f52bc6a1-c848-49e6-85de-f8f53459a624.xml")
        rg = res.release_group
        self.assertEqual("Soundtrack", rg.type_)
        self.assertEqual("Album", rg.primary_type.valueOf_)
        self.assertEqual("Soundtrack", rg.secondary_type_list.secondary_type[0].valueOf_)
