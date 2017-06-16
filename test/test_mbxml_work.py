# coding=utf-8
# Tests for parsing of work queries

import unittest
import os
import sys
# Insert .. at the beginning of path so we use this version instead
# of something that's already been installed
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from test import _common

class GetWorkTest(unittest.TestCase):
    def setUp(self):
        self.datadir = os.path.join(os.path.dirname(__file__), "data", "work")

    def testWorkAliases(self):
        res = _common.open_and_parse_test_data(self.datadir, "80737426-8ef3-3a9c-a3a6-9507afb93e93-aliases.xml")
        aliases = res.work.alias_list
        self.assertEqual(len(aliases.alias), 2)

        a0 = aliases.alias[0]
        self.assertEqual(a0.valueOf_, 'Symphonie Nr. 3 Es-Dur, Op. 55 "Eroica"')
        self.assertEqual(a0.sort_name, 'Symphonie Nr. 3 Es-Dur, Op. 55 "Eroica"')

        a1 = aliases.alias[1]
        self.assertEqual(a1.valueOf_, 'Symphony No. 3, Op. 55 "Eroica"')
        self.assertEqual(a1.sort_name, 'Symphony No. 3, Op. 55 "Eroica"')


        res = _common.open_and_parse_test_data(self.datadir, "3d7c7cd2-da79-37f4-98b8-ccfb1a4ac6c4-aliases.xml")
        aliases = res.work.alias_list
        self.assertEqual(len(aliases.alias), 10)

        a0 = aliases.alias[0]
        self.assertEqual(a0.valueOf_, "Adagio from Symphony No. 2 in E minor, Op. 27")
        self.assertEqual(a0.sort_name, "Adagio from Symphony No. 2 in E minor, Op. 27")

    def testWorkAttributes(self):
        res = _common.open_and_parse_test_data(self.datadir, "80737426-8ef3-3a9c-a3a6-9507afb93e93-aliases.xml")
        work_attrs = res.work.attribute_list
        self.assertEqual(len(work_attrs.attribute), 1)
        attr = work_attrs.attribute[0]

        self.assertEqual("Key", attr.type_)
        self.assertEqual("E-flat major", attr.valueOf_)

        res = _common.open_and_parse_test_data(self.datadir, "8e134b32-99b8-4e96-ae5c-426f3be85f4c-attributes.xml")
        work_attrs = res.work.attribute_list
        self.assertEqual(len(work_attrs.attribute), 3)

        attr = work_attrs.attribute[0]
        self.assertEqual("Makam (Ottoman, Turkish)", attr.type_)
        self.assertEqual(b"H\xc3\xbczzam".decode("utf-8"), attr.valueOf_)

        attr = work_attrs.attribute[1]
        self.assertEqual("Form (Ottoman, Turkish)", attr.type_)
        self.assertEqual(b"Pe\xc5\x9frev".decode("utf-8"), attr.valueOf_)

        attr = work_attrs.attribute[2]
        self.assertEqual("Usul (Ottoman, Turkish)", attr.type_)
        self.assertEqual("Fahte",  attr.valueOf_)

    def testWorkRelationAttributes(self):
        # Some relation attributes can contain attributes as well as text
        res = _common.open_and_parse_test_data(self.datadir, "72c9aad2-3c95-4e3e-8a01-3974f8fef8eb-series-rels.xml")

        work = res.work
        rels = work.relation_list

        self.assertEqual(1, len(rels[0].relation))

        # New attribute dict format
        attribute = rels[0].relation[0].attribute_list.attribute[0]
        self.assertEqual("BuxWV 1", attribute.value)
        self.assertEqual("number", attribute.valueOf_)
