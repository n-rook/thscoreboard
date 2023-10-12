import unittest

from replays import forms
from replays import game_ids
from replays import models
from replays.testing.test_case import ReplayTestCase
from replays.testing import test_replays


class PublishReplayFormTest(unittest.TestCase):
    def testUsesBombs_Included(self):
        f = forms.PublishReplayForm(game_ids.GameIDs.TH06, models.ReplayType.FULL_GAME)
        self.assertIn("uses_bombs", f.fields)

    def testUsesBombs_NotIncludedForTH09(self):
        f = forms.PublishReplayForm(game_ids.GameIDs.TH09, models.ReplayType.FULL_GAME)
        self.assertNotIn("uses_bombs", f.fields)

    def testUsesBombs_NotIncludedForSpellPractice(self):
        f = forms.PublishReplayForm(
            game_ids.GameIDs.TH13, models.ReplayType.SPELL_PRACTICE
        )
        self.assertNotIn("uses_bombs", f.fields)

    def testMisses_Included(self):
        f = forms.PublishReplayForm(game_ids.GameIDs.TH06, models.ReplayType.FULL_GAME)
        self.assertIn("misses", f.fields)

    def testMisses_NotIncludedForSpellPractice(self):
        f = forms.PublishReplayForm(
            game_ids.GameIDs.TH13, models.ReplayType.SPELL_PRACTICE
        )
        self.assertNotIn("misses", f.fields)


class InitializePublishReplayFormFromReplayTest(ReplayTestCase):
    def setUp(self):
        super().setUp()

        self.user = self.createUser("some-user")

    def testWithoutData(self):
        r = test_replays.CreateAsPublishedReplay(
            "th10_normal",
            user=self.user,
            category=models.Category.TAS,
            comment="Hello world",
            video_link="https://www.youtube.com/silentselenetest",
            is_good=False,
            is_clear=True,
            no_bomb=True,
            miss_count=3,
        )
        form = forms.initialize_publish_replay_form_from_replay(r)

        for field_name, expected_initial_value in [
            ("name", "AAAAAAAA"),
            ("score", 294127890),
            ("category", models.Category.TAS),
            ("comment", "Hello world"),
            ("is_good", False),
            ("is_clear", True),
            ("video_link", "https://www.youtube.com/silentselenetest"),
            ("uses_bombs", False),
            ("misses", 3),
        ]:
            with self.subTest(field_name):
                self.assertEqual(
                    form.get_initial_for_field(form.fields[field_name], field_name),
                    expected_initial_value,
                )

    def testWithData(self):
        r = test_replays.CreateAsPublishedReplay(
            "th10_normal",
            user=self.user,
            category=models.Category.STANDARD,
            comment="Hello world",
            video_link="https://www.youtube.com/silentselenetest",
            is_good=False,
            is_clear=True,
            no_bomb=True,
            miss_count=3,
        )
        form = forms.initialize_publish_replay_form_from_replay(
            r,
            data={
                "name": "AAAAAAAA",
                "score": 294127890,
                "category": models.Category.TAS,
                "comment": "Hello world",
                "is_good": True,
                "is_clear": True,
                "video_link": "https://www.youtube.com/silentselenetest",
                "no_bomb": True,
                "misses": 3,
            },
        )
        self.assertTrue(form.is_valid())

        self.assertEqual(form.cleaned_data["comment"], "Hello world")
        self.assertTrue(form.cleaned_data["is_good"])

        # Allow for the peculiar Django handling of choice fields, where the
        # cleaned_data for the choice field is cast as a string.
        self.assertCountEqual(form.changed_data, ["is_good", "category"])

    def testWithMissingFields(self):
        r = test_replays.CreateAsPublishedReplay(
            "th9_lunatic",
            user=self.user,
            category=models.Category.STANDARD,
            comment="Hello world",
            is_good=True,
            is_clear=True,
        )
        form = forms.initialize_publish_replay_form_from_replay(r)

        for field_name, expected_initial_value in [
            ("name", "AAAAAAAA"),
            ("score", 49348230),
            ("category", models.Category.STANDARD),
            ("comment", "Hello world"),
            ("is_good", True),
            ("is_clear", True),
            ("video_link", ""),
            ("misses", None),
        ]:
            with self.subTest(field_name):
                self.assertEqual(
                    form.get_initial_for_field(form.fields[field_name], field_name),
                    expected_initial_value,
                )

        self.assertNotIn("uses_bombs", form.fields)


class PublishReplayUpdateTest(ReplayTestCase):
    def setUp(self):
        super().setUp()
        self.user = self.createUser("some-user")

    def testUpdateReplay(self):
        r = test_replays.CreateAsPublishedReplay(
            "th10_normal",
            user=self.user,
            category=models.Category.STANDARD,
            comment="Hello world",
            video_link="https://www.youtube.com/silentselenetest",
            is_good=False,
            is_clear=False,
            no_bomb=False,
            miss_count=7,
        )

        form = forms.PublishReplayForm(
            gameID=game_ids.GameIDs.TH10,
            replay_type=r.replay_type,
            data={
                "name": "AAAAAAAA",
                "score": 294127890,
                "category": models.Category.TAS,
                "comment": "Hello world",
                "is_good": True,
                "is_clear": True,
                "video_link": "https://www.youtube.com/silentselenetest2",
                "no_bomb": True,
                "misses": 3,
            },
        )
        self.assertTrue(form.is_valid())
        form.update_replay(r)

        self.assertEqual(r.name, "AAAAAAAA")
        self.assertEqual(r.score, 294127890)
        self.assertEqual(r.category, models.Category.TAS)
        self.assertEqual(r.comment, "Hello world")
        self.assertTrue(r.is_good)
        self.assertTrue(r.is_clear)
        self.assertEqual(r.video_link, "https://www.youtube.com/silentselenetest2")
        self.assertTrue(r.no_bomb)
        self.assertEqual(r.miss_count, 3)


class PublishReplayWithoutFileFormTest(ReplayTestCase):
    def testPvpReplayType_Included(self):
        th03 = models.Game.objects.get(game_id="th03")
        f = forms.PublishReplayWithoutFileForm(game=th03)
        replay_type_choices = [entry[1] for entry in f.fields["replay_type"].choices]
        self.assertIn("PVP", replay_type_choices)

    def testPvpReplayType_NotIncluded(self):
        game_ids_without_pvp = [
            game_ids.GameIDs.TH01,
            game_ids.GameIDs.TH02,
            game_ids.GameIDs.TH04,
            game_ids.GameIDs.TH05,
        ]
        for game_id in game_ids_without_pvp:
            with self.subTest():
                game = models.Game.objects.get(game_id=game_id)
                f = forms.PublishReplayWithoutFileForm(game=game)
                replay_type_choices = [
                    entry[1] for entry in f.fields["replay_type"].choices
                ]
                self.assertNotIn("PVP", replay_type_choices)
