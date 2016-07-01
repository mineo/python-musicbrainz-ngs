import mock
import hashlib
import musicbrainzngs.cache


from re import compile
from test import _common


class DummyCache(musicbrainzngs.cache.BaseCache):
    pass


class CacheTest(_common.RequestsMockingTestCase):
    """ Test that we can cache results"""

    def setUp(self):
        super(CacheTest, self).setUp()
        musicbrainzngs.set_useragent("a", "1")
        musicbrainzngs.set_rate_limit(False)
        self.cache = musicbrainzngs.cache.BaseCache()
        musicbrainzngs.set_cache(self.cache)

    def tearDown(self):
        super(CacheTest, self).tearDown()
        musicbrainzngs.set_cache(None)

    @mock.patch('musicbrainzngs.musicbrainz.parser_fun')
    @mock.patch('musicbrainzngs.cache.BaseCache.get', side_effect=musicbrainzngs.cache.NotInCache)
    def test_cache_is_set_after_mb_request(self, *mocks):
        """ Check the cache is called when set on the client"""
        self.m.get(compile("ws/2/.*/*"), text="return_value")
        expected_kwargs = {
            'args': [],
            'method': 'GET',
            'url': 'http://musicbrainz.org/ws/2/artist/mbid',
        }
        expected_kwargs['key'] = self.cache.build_key(**expected_kwargs)
        h = hashlib.sha1(expected_kwargs['url'].encode('utf-8')).hexdigest()

        self.assertEqual(expected_kwargs['key'], h)

        with mock.patch('musicbrainzngs.cache.BaseCache.set') as cache:
            musicbrainzngs.get_artist_by_id('mbid')
            cache.assert_called_once_with(value='return_value', **expected_kwargs)

    @mock.patch('musicbrainzngs.musicbrainz.parser_fun', side_effect=lambda v: v)
    @mock.patch('musicbrainzngs.cache.BaseCache.set')
    def test_cache_get_is_called_before_request(self, *mocks):
        expected_kwargs = {
            'args': [],
            'method': 'GET',
            'url': 'http://musicbrainz.org/ws/2/artist/mbid',
        }

        expected_kwargs['key'] = self.cache.build_key(**expected_kwargs)
        h = hashlib.sha1(expected_kwargs['url'].encode('utf-8')).hexdigest()

        self.assertEqual(expected_kwargs['key'], h)

        with mock.patch('musicbrainzngs.cache.BaseCache.get', return_value='value') as cache:
            r = musicbrainzngs.get_artist_by_id('mbid')
            cache.assert_called_once_with(**expected_kwargs)
            self.assertEqual(r, 'value')

    @mock.patch('musicbrainzngs.musicbrainz.parser_fun', side_effect=lambda v: v)
    def test_basic_dict_cache(self, parser):
        self.m.get(compile("ws/2/.*/*"), text="return_value")
        cache = musicbrainzngs.cache.DictCache()
        musicbrainzngs.set_cache(cache)

        # first, we populate the cache
        r = musicbrainzngs.get_artist_by_id('mbid')
        self.assertEqual(r, 'return_value')
        self.assertEqual(self.m.call_count, 1)


        with mock.patch.object(cache, 'get', wraps=cache.get) as mocked:
            # now we make the same request, so the cache is used
            r = musicbrainzngs.get_artist_by_id('mbid')
            self.assertEqual(r, 'return_value')

            mocked.assert_called_once()

            # read should not have been called again
            self.assertEqual(self.m.call_count, 1)
