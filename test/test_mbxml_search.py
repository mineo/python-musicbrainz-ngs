import unittest
import os
import sys
# Insert .. at the beginning of path so we use this version instead
# of something that's already been installed
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import musicbrainzngs
from musicbrainzngs import mbxml
from test import _common


DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

@unittest.skip("Yeah, sorry, no searches yet :(")
class UrlTest(unittest.TestCase):
    """ Test that the correct URL is generated when a search query is made """

    def setUp(self):
        self.opener = _common.FakeOpener(b"<response/>")
        musicbrainzngs.compat.build_opener = lambda *args: self.opener

        musicbrainzngs.set_useragent("a", "1")
        musicbrainzngs.set_rate_limit(False)

    def testSearchArtist(self):
        musicbrainzngs.search_artists("Dynamo Go")
        self.assertEqual("http://musicbrainz.org/ws/2/artist/?query=Dynamo+Go", self.opener.get_url())

    def testSearchEvent(self):
        musicbrainzngs.search_events("woodstock")
        self.assertEqual("http://musicbrainz.org/ws/2/event/?query=woodstock", self.opener.get_url())

    def testSearchLabel(self):
        musicbrainzngs.search_labels("Waysafe")
        self.assertEqual("http://musicbrainz.org/ws/2/label/?query=Waysafe", self.opener.get_url())

    def testSearchPlace(self):
        musicbrainzngs.search_places("Fillmore")
        self.assertEqual("http://musicbrainz.org/ws/2/place/?query=Fillmore", self.opener.get_url())

    def testSearchRelease(self):
        musicbrainzngs.search_releases("Affordable Pop Music")
        self.assertEqual("http://musicbrainz.org/ws/2/release/?query=Affordable+Pop+Music", self.opener.get_url())

    def testSearchReleaseGroup(self):
        musicbrainzngs.search_release_groups("Affordable Pop Music")
        self.assertEqual("http://musicbrainz.org/ws/2/release-group/?query=Affordable+Pop+Music", self.opener.get_url())

    def testSearchRecording(self):
        musicbrainzngs.search_recordings("Thief of Hearts")
        self.assertEqual("http://musicbrainz.org/ws/2/recording/?query=Thief+of+Hearts", self.opener.get_url())

    def testSearchWork(self):
        musicbrainzngs.search_works("Fountain City")
        self.assertEqual("http://musicbrainz.org/ws/2/work/?query=Fountain+City", self.opener.get_url())


@unittest.skip("Yeah, sorry, no searches yet :(")
class SearchArtistTest(unittest.TestCase):
    def testFields(self):
        fn = os.path.join(DATA_DIR, "search-artist.xml")
        with open(fn, 'rb') as msg:
            res = mbxml.parse_message(msg.read())
        self.assertEqual(25, len(res.artist_list.artist))
        self.assertEqual(349, res.artist_list.count)
        one = res.artist_list.artist[0]
        # Score is a key that is only in search results -
        # so check for it here
        self.assertEqual("100", one["ext:score"])

@unittest.skip("Yeah, sorry, no searches yet :(")
class SearchReleaseTest(unittest.TestCase):
    def testFields(self):
        fn = os.path.join(DATA_DIR, "search-release.xml")
        with open(fn, 'rb') as msg:
            res = mbxml.parse_message(msg.read())
        self.assertEqual(25, len(res.release_list.release))
        self.assertEqual(16739, res.release_list.count)
        one = res.release_list.release[0]
        self.assertEqual("100", one["ext:score"])

        # search results have a medium-list/track-count element
        self.assertEqual(4, one["medium-track-count"])
        self.assertEqual(1, one.medium_list.count)
        self.assertEqual("CD", one.medium_list.medium[0].format)

@unittest.skip("Yeah, sorry, no searches yet :(")
class SearchReleaseGroupTest(unittest.TestCase):
    def testFields(self):
        fn = os.path.join(DATA_DIR, "search-release-group.xml")
        with open(fn, 'rb') as msg:
            res = mbxml.parse_message(msg.read())
        self.assertEqual(25, len(res["release-group-list"]))
        self.assertEqual(14641, res["release-group-count"])
        one = res["release-group-list"][0]
        self.assertEqual("100", one["ext:score"])

@unittest.skip("Yeah, sorry, no searches yet :(")
class SearchWorkTest(unittest.TestCase):
    def testFields(self):
        fn = os.path.join(DATA_DIR, "search-work.xml")
        with open(fn, 'rb') as msg:
            res = mbxml.parse_message(msg.read())
        self.assertEqual(25, len(res.work_list.work))
        self.assertEqual(174, res.work_list.count)
        one = res.work_list.work[0]
        self.assertEqual("100", one["ext:score"])

@unittest.skip("Yeah, sorry, no searches yet :(")
class SearchLabelTest(unittest.TestCase):
    def testFields(self):
        fn = os.path.join(DATA_DIR, "search-label.xml")
        with open(fn, 'rb') as msg:
            res = mbxml.parse_message(msg.read())
        self.assertEqual(1, len(res.label_list.label))
        self.assertEqual(1, res.label_list.count)
        one = res.label_list.label[0]
        self.assertEqual("100", one["ext:score"])

@unittest.skip("Yeah, sorry, no searches yet :(")
class SearchRecordingTest(unittest.TestCase):
    def testFields(self):
        fn = os.path.join(DATA_DIR, "search-recording.xml")
        with open(fn, 'rb') as msg:
            res = mbxml.parse_message(msg.read())
        self.assertEqual(25, len(res.recording_list.recording))
        self.assertEqual(1258, res.recording_list.count)
        one = res.recording_list.recording[0]
        self.assertEqual("100", one["ext:score"])

@unittest.skip("Yeah, sorry, no searches yet :(")
class SearchInstrumentTest(unittest.TestCase):
    def testFields(self):
        fn = os.path.join(DATA_DIR, "search-instrument.xml")
        with open(fn, 'rb') as msg:
            res = mbxml.parse_message(msg.read())
        self.assertEqual(23, len(res.instrument_list.instrument))
        self.assertEqual(23, res.instrument_list.count)
        one = res.instrument_list.instrument[0]
        self.assertEqual("100", one["ext:score"])
        end = res.instrument_list.instrument[-1]
        self.assertEqual("29", end["ext:score"])

@unittest.skip("Yeah, sorry, no searches yet :(")
class SearchPlaceTest(unittest.TestCase):
    def testFields(self):
        fn = os.path.join(DATA_DIR, "search-place.xml")
        with open(fn, 'rb') as msg:
            res = mbxml.parse_message(msg.read())
        self.assertEqual(14, res.place_list.count)
        self.assertEqual(14, len(res.place_list.place))
        one = res.place_list.place[0]
        self.assertEqual("100", one["ext:score"])
        two = res.place_list.place[1]
        self.assertEqual("63", two["ext:score"])
        self.assertEqual("Southampton", two.disambiguation)

@unittest.skip("Yeah, sorry, no searches yet :(")
class SearchEventTest(unittest.TestCase):
    def testFields(self):
        fn = os.path.join(DATA_DIR, "search-event.xml")
        with open(fn, 'rb') as msg:
            res = mbxml.parse_message(msg.read())
        self.assertEqual(3, res.event_list.count)
        self.assertEqual(3, len(res.event_list.event))
        one = res.event_list.event[0]
        self.assertEqual("100", one["ext:score"])
        two = res.event_list.event[1]
        self.assertEqual(1, len(two["place-relation-list"]))
