from unittest import mock

from django import test as django_test
from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import HttpResponse
from django import urls

from replays import models
from replays.views import create_replay
from replays import game_ids
from replays import replay_parsing
from replays.testing import test_case
from replays.testing import test_replays


class CreateReplayTestCase(test_case.ReplayTestCase):
    def setUp(self):
        super().setUp()
        self.factory = django_test.RequestFactory()
        self.user = self.createUser("some-user")

    def testOrdinaryReplay(self):
        replay_file_contents = test_replays.GetRaw("th10_normal")
        replay_info = replay_parsing.Parse(replay_file_contents)

        temp_replay = models.TemporaryReplayFile(
            user=self.user, replay=replay_file_contents
        )
        temp_replay.save()

        request = self.factory.post(
            urls.reverse("publish_replay", kwargs={"temp_replay_id": temp_replay.id}),
            data={
                "score": replay_info.score,
                "category": models.Category.STANDARD,
                "comment": "Hello, world!",
                "is_good": True,
                "is_clear": True,
                "video_link": "",
                "name": replay_info.name,
                "uses_bombs": True,
                "misses": 5,
            },
        )
        request.user = self.user
        response = create_replay.publish_replay(request, temp_replay.id)
        self.assertEqual(response.status_code, 302)

        target = urls.resolve(response.url)
        replay = models.Replay.objects.get(id=target.captured_kwargs["replay_id"])

        self.assertEqual(replay.shot.game.game_id, target.captured_kwargs["game_id"])
        self.assertEqual(replay.score, replay_info.score)
        self.assertEqual(replay.category, models.Category.STANDARD)
        self.assertEqual(replay.comment, "Hello, world!")
        self.assertTrue(replay.is_good)
        self.assertTrue(replay.is_clear)
        self.assertEqual(replay.video_link, "")
        self.assertEqual(replay.name, replay_info.name)
        self.assertFalse(replay.no_bomb)
        self.assertEqual(replay.miss_count, 5)

        with self.assertRaises(models.TemporaryReplayFile.DoesNotExist):
            models.TemporaryReplayFile.objects.get(id=temp_replay.id)

    def testTh03StillAllowsPublishingWithoutAFile(self):
        game = models.Game.objects.get(game_id=game_ids.GameIDs.TH03)
        self.assertTrue(game.has_replays)
        self.assertTrue(game.AllowsReplaylessSubmissions())

        request = self.factory.get(f"/replays/publish/{game.game_id}")
        request.user = self.user
        response = create_replay.publish_replay_no_file(request, game.game_id)
        self.assertEqual(response.status_code, 200)

    def testTh03AppearsInBothUploadLists(self):
        request = self.factory.get("/replays/upload")
        request.user = self.user
        with mock.patch.object(
            create_replay, "render", return_value=HttpResponse()
        ) as render:
            create_replay.upload_file(request)

        context = render.call_args.args[2]
        replay_game_ids = [game.game_id for game in context["replay_games"]]
        no_replay_game_ids = [game.game_id for game in context["no_replay_games"]]
        self.assertIn(game_ids.GameIDs.TH03, replay_game_ids)
        self.assertIn(game_ids.GameIDs.TH03, no_replay_game_ids)

    def testOldTh03FormatsRequireInstallerUpgrade(self):
        message = (
            "This PoDD replay uses an older format. Please use the Replay Patch "
            "installer or Data Manager to update it to V14 before uploading."
        )
        for version in (11, 12, 13):
            with self.subTest(version=version):
                request = self.factory.post(
                    "/replays/upload",
                    data={
                        "replay_file": SimpleUploadedFile(
                            f"TH3R{version}.RPY", f"T3RPLY{version}".encode()
                        )
                    },
                )
                request.user = self.user
                response = create_replay.upload_file(request)
                self.assertContains(response, message)
