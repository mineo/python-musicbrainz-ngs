# -*- coding: utf-8 -*-
# Tests for parsing instrument queries

import unittest
import os
import sys
# Insert .. at the beginning of path so we use this version instead
# of something that's already been installed
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from test import _common
import musicbrainzngs

class GetInstrumentTest(unittest.TestCase):
    def setUp(self):
        self.datadir = os.path.join(os.path.dirname(__file__), "data", "instrument")

    def testData(self):
        res = _common.open_and_parse_test_data(self.datadir, "9447c0af-5569-48f2-b4c5-241105d58c91.xml")
        inst = res.instrument

        self.assertEqual(inst.id, "9447c0af-5569-48f2-b4c5-241105d58c91")
        self.assertEqual(inst.name, "bass saxophone")
        self.assertEqual(inst.type_, "Wind instrument")
        self.assertTrue(inst.description.startswith("The bass saxophone"))

    def testAliases(self):
        res = _common.open_and_parse_test_data(self.datadir, "6505f98c-f698-4406-8bf4-8ca43d05c36f-aliases.xml")
        inst = res.instrument

        aliases = inst.alias_list
        self.assertEqual(len(aliases.alias), 14)
        self.assertEqual(aliases.alias[1].locale, "it")
        self.assertEqual(aliases.alias[1].type_, "Instrument name")
        self.assertEqual(aliases.alias[1].primary, "primary")
        self.assertEqual(aliases.alias[1].sort_name, "Basso")
        self.assertEqual(aliases.alias[1].valueOf_, "Basso")


    def testTags(self):
        res = _common.open_and_parse_test_data(self.datadir, "6505f98c-f698-4406-8bf4-8ca43d05c36f-tags.xml")
        inst = res.instrument

        tags = inst.tag_list
        self.assertEqual(len(tags.tag), 3)
        self.assertEqual(tags.tag[0].name, "fixme")
        self.assertEqual(tags.tag[0].count, 1)

    def testUrlRels(self):
        res = _common.open_and_parse_test_data(self.datadir, "d00cec5f-f9bc-4235-a54f-6639a02d4e4c-url-rels.xml")
        inst = res.instrument

        rels = inst.relation_list
        self.assertEqual(len(rels[0].relation), 3)
        self.assertEqual(rels[0].relation[0].type_, "information page")
        self.assertEqual(rels[0].relation[0].type_id, "0e62afec-12f3-3d0f-b122-956207839854")
        self.assertTrue(rels[0].relation[0].target.valueOf_.startswith("http://en.wikisource"))

    def testAnnotations(self):
        res = _common.open_and_parse_test_data(self.datadir, "d00cec5f-f9bc-4235-a54f-6639a02d4e4c-annotation.xml")
        inst = res.instrument
        self.assertEqual(inst.annotation.text, "Hornbostel-Sachs: 412.22")

    def testInstrumentRels(self):
        res = _common.open_and_parse_test_data(self.datadir, "01ba56a2-4306-493d-8088-c7e9b671c74e-instrument-rels.xml")
        inst = res.instrument

        rels = inst.relation_list[0].relation
        self.assertEqual(len(rels), 3)
        self.assertEqual(rels[1].type_, "children")
        self.assertEqual(rels[1].type_id, "12678b88-1adb-3536-890e-9b39b9a14b2d")
        self.assertEqual(rels[1].target.valueOf_, "ad09a4ed-d1b6-47c3-ac85-acb531244a4d")
        self.assertEqual(rels[1].instrument.id, "ad09a4ed-d1b6-47c3-ac85-acb531244a4d")
        self.assertTrue(rels[1].instrument.name.startswith(b"kemen\xc3\xa7e".decode("utf-8")))

    def testDisambiguation(self):
        res = _common.open_and_parse_test_data(self.datadir, "dabdeb41-560f-4d84-aa6a-cf22349326fe.xml")
        inst = res.instrument
        self.assertEqual(inst.disambiguation, "lute")
