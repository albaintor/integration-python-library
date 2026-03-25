import unittest
from ucapi.media_player import SearchMediaFilter, MediaClass


class TestMediaPlayer(unittest.TestCase):
    def test_search_media_filter_media_classes(self):
        """Test SearchMediaFilter media_classes with standard and custom values."""
        # Test with standard MediaClass
        smf = SearchMediaFilter(media_classes=[MediaClass.ALBUM, MediaClass.TRACK])
        self.assertEqual(smf.media_classes, [MediaClass.ALBUM, MediaClass.TRACK])

        # Test with strings that match MediaClass
        smf = SearchMediaFilter(media_classes=["album", "track"])
        self.assertEqual(smf.media_classes, [MediaClass.ALBUM, MediaClass.TRACK])

        # Test with custom string values
        try:
            smf = SearchMediaFilter(media_classes=["custom_class", "another_one"])
            self.assertEqual(smf.media_classes, ["custom_class", "another_one"])
        except ValueError as e:
            self.fail(
                f"SearchMediaFilter raised ValueError for custom media classes: {e}"
            )

    def test_search_media_filter_mixed_classes(self):
        """Test SearchMediaFilter with a mix of MediaClass and custom strings."""
        try:
            smf = SearchMediaFilter(media_classes=[MediaClass.ALBUM, "custom_class"])
            self.assertEqual(smf.media_classes, [MediaClass.ALBUM, "custom_class"])
        except ValueError as e:
            self.fail(
                f"SearchMediaFilter raised ValueError for mixed media classes: {e}"
            )

    def test_search_media_filter_none(self):
        """Test SearchMediaFilter with None media_classes."""
        smf = SearchMediaFilter(media_classes=None)
        self.assertIsNone(smf.media_classes)

    def test_search_media_filter_from_dict(self):
        """Test SearchMediaFilter.from_dict with custom values."""
        data = {
            "media_classes": ["album", "custom_class"],
            "artist": "Some Artist",
            "album": "Some Album",
        }
        try:
            smf = SearchMediaFilter.from_dict(data)
            self.assertEqual(smf.media_classes, [MediaClass.ALBUM, "custom_class"])
            self.assertEqual(smf.artist, "Some Artist")
            self.assertEqual(smf.album, "Some Album")
        except ValueError as e:
            self.fail(
                f"SearchMediaFilter.from_dict raised ValueError for custom media classes: {e}"
            )


if __name__ == "__main__":
    unittest.main()
