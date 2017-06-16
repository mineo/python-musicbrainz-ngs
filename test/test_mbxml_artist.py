# Tests for parsing of artist queries

import unittest
import os
import sys
# Insert .. at the beginning of path so we use this version instead
# of something that's already been installed
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from test import _common

class GetArtistTest(unittest.TestCase):
    def setUp(self):
        self.datadir = os.path.join(os.path.dirname(__file__), "data", "artist")

    def testArtistAliases(self):
        res = _common.open_and_parse_test_data(self.datadir, "0e43fe9d-c472-4b62-be9e-55f971a023e1-aliases.xml")
        aliases = res.artist.alias_list
        self.assertEqual(len(aliases.alias), 28)

        a0 = aliases.alias[0]
        self.assertEqual(a0.valueOf_, "Prokofief")
        self.assertEqual(a0.sort_name, "Prokofief")

        a17 = aliases.alias[17]
        self.assertEqual(a17.valueOf_, "Sergei Sergeyevich Prokofiev")
        self.assertEqual(a17.sort_name, "Prokofiev, Sergei Sergeyevich")
        self.assertEqual(a17.locale, "en")
        self.assertEqual(a17.primary, "primary")

    def testArtistTargets(self):
        res = _common.open_and_parse_test_data(self.datadir, "b3785a55-2cf6-497d-b8e3-cfa21a36f997-artist-rels.xml")
        self.assertTrue(hasattr(res.artist.relation_list[0].relation[0], "target_credit"))
        self.assertEqual(res.artist.relation_list[0].relation[0].target_credit, "TAO")
