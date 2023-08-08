import unittest
from replays.lib.video_embed import get_video_embed_link


class YouTubeEmbedTestCase(unittest.TestCase):
    def testYouTubeWatch(self):
        self.assertEqual(
            get_video_embed_link(
                "https://www.youtube.com/watch?v=pFlhyEJ6XbM&v=f2xvnIDMJLE"
            ),
            "https://www.youtube.com/embed/pFlhyEJ6XbM",
        )

    def testYouTubeShortLink(self):
        self.assertEqual(
            get_video_embed_link("https://youtu.be/_LSltayY-Aw/Thank-you-morth"),
            "https://www.youtube.com/embed/_LSltayY-Aw",
        )

    def testYouTubeShortLinkWithQuery(self):
        self.assertEqual(
            get_video_embed_link("https://youtu.be/f2xvnIDMJLE?v=TaQ6JYS4fLM"),
            "https://www.youtube.com/embed/TaQ6JYS4fLM",
        )

    def testYouTubeShortLinkMultipathWithQuery(self):
        self.assertEqual(
            get_video_embed_link(
                "https://youtu.be/y8nBF2crayo/pawn-to-e10?v=TaQ6JYS4fLM"
            ),
            "https://www.youtube.com/embed/TaQ6JYS4fLM",
        )

    def testYouTubeShortsWithQueryV(self):
        self.assertEqual(
            get_video_embed_link(
                "https://www.youtube.com/shorts/9ZnrihX2lVY?v=8XD9_zW6ozo&v=Deez-Nuts"
            ),
            "https://www.youtube.com/embed/8XD9_zW6ozo",
        )

    def testYouTubeShorts(self):
        self.assertEqual(
            get_video_embed_link("https://www.youtube.com/shorts/9ZnrihX2lVY"),
            "https://www.youtube.com/embed/9ZnrihX2lVY",
        )


class TwitchEmbedTestCase(unittest.TestCase):
    def testTwitchMultipath(self):
        self.assertEqual(
            get_video_embed_link(
                "https://www.twitch.tv/videos/1830919460/deeznuts?thank-you-morth=true"
            ),
            "https://player.twitch.tv/?video=v1830919460&parent=www.silentselene.net&autoplay=false",
        )

    def testTwitchQueryString(self):
        self.assertEqual(
            get_video_embed_link(
                "https://www.twitch.tv/videos/1830919460?thank-you-morth=true"
            ),
            "https://player.twitch.tv/?video=v1830919460&parent=www.silentselene.net&autoplay=false",
        )

    def testTwitchClip(self):
        self.assertEqual(
            get_video_embed_link(
                "https://www.twitch.tv/touhou_replay_showcase/clip/PatientCredulousGoshawkDoubleRainbow?filter=clips&range=all&sort=time"
            ),
            "https://clips.twitch.tv/embed?clip=PatientCredulousGoshawkDoubleRainbow&parent=www.silentselene.net&autoplay=false",
        )

    def testTwitchClipMultipath(self):
        self.assertEqual(
            get_video_embed_link(
                "https://www.twitch.tv/touhou_replay_showcase/clip/PatientCredulousGoshawkDoubleRainbow/DeezNuts"
            ),
            None,
        )


class BilibiliEmbedTestCase(unittest.TestCase):
    def testBilibili(self):
        self.assertEqual(
            get_video_embed_link("https://www.bilibili.com/video/BV1LW4y1H7JS"),
            "https://player.bilibili.com/player.html?bvid=BV1LW4y1H7JS&autoplay=false",
        )

    def testBilibiliTrailingSlash(self):
        self.assertEqual(
            get_video_embed_link("https://www.bilibili.com/video/BV1LW4y1H7JS/"),
            "https://player.bilibili.com/player.html?bvid=BV1LW4y1H7JS&autoplay=false",
        )

    def testBilibiliMultipath(self):
        self.assertEqual(
            get_video_embed_link("https://www.bilibili.com/video/BV1LW4y1H7JS/d"),
            None,
        )
