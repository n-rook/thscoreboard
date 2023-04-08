from django import test

from users import models
from users import parse_invite_csv


def _CreateUser(username="somebody", password="pw", email="somebody@example.com"):
    return models.User.objects.create_user(
        username=username,
        password=password,
        email=email,
    )


class ParseInviteTestCase(test.TestCase):
    def setUp(self) -> None:
        self._staff = _CreateUser(username="miko", email="admin@example.com")

    def _CreateInvite(self, username="somebody", email="somebody@example.com"):
        models.InvitedUser.CreateInvite(
            username=username, email=email, inviter=self._staff
        )

    def testWellFormed(self):
        result = parse_invite_csv.Parse(
            "Reimu,reimu@example.com\nMarisa,lasers@example.com\n"
        )
        self.assertEqual(len(result), 2)

        reimu = result[0]
        self.assertEqual(reimu.username, "Reimu")
        self.assertEqual(reimu.email, "reimu@example.com")
        self.assertFalse(reimu.errors)
        self.assertFalse(reimu.warnings)

        marisa = result[1]
        self.assertEqual(marisa.username, "Marisa")
        self.assertEqual(marisa.email, "lasers@example.com")
        self.assertFalse(marisa.errors)
        self.assertFalse(marisa.warnings)

    def testComma(self):
        result = parse_invite_csv.Parse('"mi,zuchi","jailbreak,king@example.com"')
        self.assertEqual(len(result), 1)

        mizuchi = result[0]
        self.assertEqual(mizuchi.username, "mi,zuchi")
        self.assertEqual(mizuchi.email, "jailbreak,king@example.com")

    def testNoUsername(self):
        result = parse_invite_csv.Parse(",ghost@example.com")
        self.assertEqual(len(result), 1)

        ghost = result[0]
        self.assertEqual(ghost.email, "ghost@example.com")
        self.assertIn("No username", ghost.errors_str)

    def testUsernameAlreadyUsed(self):
        _CreateUser(username="reimu", email="reimu@example.com")

        result = parse_invite_csv.Parse("reimu,hakurei@example.com")
        self.assertEqual(len(result), 1)

        reimu = result[0]
        self.assertEqual(reimu.email, "hakurei@example.com")
        self.assertIn("User already exists (reimu@example.com)", reimu.errors_str)

    def testUsernameAlreadyInvited(self):
        self._CreateInvite(username="reimu", email="reimu@example.com")

        result = parse_invite_csv.Parse("reimu,hakurei@example.com")
        self.assertEqual(len(result), 1)

        reimu = result[0]
        self.assertEqual(reimu.username, "reimu")
        self.assertFalse(reimu.errors_str)
        self.assertIn("User already invited (reimu@example.com)", reimu.warnings_str)

    def testNoEmailField(self):
        result = parse_invite_csv.Parse("ghost")
        self.assertEqual(len(result), 1)

        ghost = result[0]
        self.assertEqual(ghost.username, "ghost")
        self.assertIn("No email", ghost.errors_str)

    def testNoEmail(self):
        result = parse_invite_csv.Parse("ghost,")
        self.assertEqual(len(result), 1)

        ghost = result[0]
        self.assertEqual(ghost.username, "ghost")
        self.assertIn("No email", ghost.errors_str)

    def testEmailAlreadyUsed(self):
        _CreateUser(username="reimu", email="reimu@example.com")

        result = parse_invite_csv.Parse("hakurei-reimu,reimu@example.com")
        self.assertEqual(len(result), 1)

        reimu = result[0]
        self.assertEqual(reimu.email, "reimu@example.com")
        self.assertIn("User already exists (reimu)", reimu.errors_str)

    def testEmailAlreadyInvited(self):
        self._CreateInvite(username="reimu", email="reimu@example.com")

        result = parse_invite_csv.Parse("reimu-hakurei,reimu@example.com")
        self.assertEqual(len(result), 1)

        reimu = result[0]
        self.assertEqual(reimu.username, "reimu-hakurei")
        self.assertFalse(reimu.errors_str)
        self.assertIn("User already invited (reimu)", reimu.warnings_str)
