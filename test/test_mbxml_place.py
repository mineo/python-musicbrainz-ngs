# Tests for parsing of place results

import unittest
import os
import sys
# Insert .. at the beginning of path so we use this version instead
# of something that's already been installed
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from test import _common


class PlaceTest(unittest.TestCase):
    def setUp(self):
        self.datadir = os.path.join(os.path.dirname(__file__), "data", "place")

    def testPlace(self):
        filename = "0c79cdbb-acd6-4e30-aaa3-a5c8d6b36a48-aliases-tags.xml"
        res = _common.open_and_parse_test_data(self.datadir, filename)

        p = res.place
        self.assertEqual("All Saints' Church", p.name)
        self.assertEqual("East Finchley, Durham Road", p.disambiguation)
        self.assertEqual("38 Durham Road, London N2 9DP, United Kingdom", p.address)
        self.assertEqual('51.591812', p.coordinates.latitude)
        self.assertEqual('-0.159699', p.coordinates.longitude)
        self.assertEqual("f03d09b3-39dc-4083-afd6-159e3f0d462f", p.area.id)
        self.assertEqual("1891", p.life_span.begin)
        self.assertEqual("All Saints' Durham Road", p.alias_list.alias[0].valueOf_)
        self.assertEqual("type=church", p.tag_list.tag[0].name)
        self.assertEqual(1, p.tag_list.tag[0].count)

    def testListFromBrowse(self):
        filename = "browse-area-74e50e58-5deb-4b99-93a2-decbb365c07f-annotation.xml"
        res = _common.open_and_parse_test_data(self.datadir, filename)

        self.assertEqual(395, res.place_list.count)
        self.assertEqual(25, len(res.place_list.place))

        self.assertTrue(res.place_list.place[13].annotation.text.startswith("was later renamed"))
