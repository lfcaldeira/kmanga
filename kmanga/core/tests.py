from django.test import TestCase

from core.models import AltName
from core.models import Genre
from core.models import Issue
from core.models import Manga
from core.models import Source
from core.models import SourceLanguage
from core.models import Subscription
from registration.models import UserProfile


class SourceTestCase(TestCase):
    fixtures = ['registration.json', 'core.json']

    def test_str(self):
        """Test source representation."""
        self.assertEqual(str(Source.objects.get(pk=1)),
                         'Source 1 (http://source1.com)')


class SourceLanguageTestCase(TestCase):
    fixtures = ['registration.json', 'core.json']

    def test_str(self):
        """Test source language representation."""
        self.assertEqual(str(SourceLanguage.objects.get(pk=1)),
                         'English')


class GenreTestCase(TestCase):
    fixtures = ['registration.json', 'core.json']

    def test_str(self):
        """Test genre representation."""
        self.assertEqual(str(Genre.objects.get(pk=1)),
                         'source1_genre1')


class MangaTestCase(TestCase):
    fixtures = ['registration.json', 'core.json']

    def test_full_text_search_basic(self):
        """Test basic FTS operations."""
        # Initially the materialized view empty
        Manga.objects.refresh()

        # Search for a common keyword
        self.assertEqual(
            len(Manga.objects.search('Description')), 4)

        # Search for specific keyword in the name
        m = Manga.objects.get(name='Manga 1')
        old_value = m.name
        m.name = 'keyword'
        m.save()
        Manga.objects.refresh()
        q = Manga.objects.search('keyword')
        self.assertEqual(len(q), 1)
        self.assertEqual(iter(q).next(), m)
        m.name = old_value
        m.save()
        Manga.objects.refresh()
        self.assertEqual(
            len(Manga.objects.search('keyword')), 0)

        # Search for specific keyword in alt_name
        q = Manga.objects.search('One')
        self.assertEqual(len(q), 1)
        self.assertEqual(
            iter(q).next(),
            Manga.objects.get(name='Manga 1'))

        q = Manga.objects.search('Two')
        self.assertEqual(len(q), 1)
        self.assertEqual(
            iter(q).next(),
            Manga.objects.get(name='Manga 2'))

        # Search for specific keyword in description
        m = Manga.objects.get(name='Manga 3')
        old_value = m.description
        m.description += ' keyword'
        m.save()
        Manga.objects.refresh()
        q = Manga.objects.search('keyword')
        self.assertEqual(len(q), 1)
        self.assertEqual(iter(q).next(), m)
        m.description = old_value
        m.save()
        Manga.objects.refresh()
        self.assertEqual(
            len(Manga.objects.search('keyword')), 0)

    def test_full_text_search_rank(self):
        """Test FTS ranking."""
        # Initially the materialized view empty
        Manga.objects.refresh()

        # Add the same keywork in the name and in the description.
        # Because the name is more important, the first result must be
        # the one with the keyword in it.
        m1 = Manga.objects.get(name='Manga 3')
        m1.name = 'keyword'
        m1.save()
        m2 = Manga.objects.get(name='Manga 4')
        m2.description += ' keyword'
        m2.save()
        Manga.objects.refresh()

        q = Manga.objects.search('keyword')
        self.assertEqual(len(q), 2)
        _iter = iter(q)
        self.assertEqual(_iter.next(), m1)
        self.assertEqual(_iter.next(), m2)

    def test_full_text_search_index(self):
        """Test indexing (__getitem__) FTS operations."""
        # Initially the materialized view empty
        Manga.objects.refresh()

        ms1 = list(Manga.objects.search('Description'))
        ms2 = list(Manga.objects.search('Description')[1])
        ms3 = list(Manga.objects.search('Description')[1:3])
        self.assertEqual(len(ms1), 4)
        self.assertEqual(len(ms2), 1)
        self.assertEqual(len(ms3), 2)
        self.assertEqual(ms1.index(ms2[0]), 1)
        self.assertEqual(ms1.index(ms3[0]), 1)
        self.assertEqual(ms1.index(ms3[1]), 2)

    def test_latests(self):
        """Test the recovery of updated mangas."""
        # Random order where we expect the mangas
        names = ('Manga 2', 'Manga 4', 'Manga 1', 'Manga 3')
        for name in reversed(names):
            issue = Issue.objects.get(name='%s issue 1' % name.lower())
            issue.name += ' - %s' % name
            issue.save()

        for manga, name in zip(Manga.objects.latests(), names):
            self.assertEqual(manga.name, name)

    def test_str(self):
        """Test manga representation."""
        self.assertEqual(str(Manga.objects.get(pk=1)),
                         'Manga 1')

    def test_subscribe(self):
        """Test the method to subscrive an user to a manga."""
        # The fixture have 4 mangas and two users.  The last manga
        # have no subscrivers, and `Manga 3` is `deleted`
        user = UserProfile.objects.get(pk=1).user

        self.assertTrue(
            Manga.objects.get(name='Manga 1').is_subscribed(user))
        self.assertTrue(
            Manga.objects.get(name='Manga 2').is_subscribed(user))
        self.assertFalse(
            Manga.objects.get(name='Manga 3').is_subscribed(user))
        self.assertFalse(
            Manga.objects.get(name='Manga 4').is_subscribed(user))

        manga = Manga.objects.get(name='Manga 4')
        manga.subscribe(user)
        self.assertTrue(manga.is_subscribed(user))
        self.assertEqual(manga.subscription_set.count(), 1)
        self.assertEqual(manga.subscription_set.all()[0].user, user)

        manga = Manga.objects.get(name='Manga 3')
        manga.subscribe(user)
        self.assertTrue(manga.is_subscribed(user))
        self.assertEqual(manga.subscription_set.count(), 1)
        self.assertEqual(manga.subscription_set.all()[0].user, user)
        self.assertEqual(
            Subscription.all_objects.filter(user=user).count(), 4)


class AltNameTestCase(TestCase):
    fixtures = ['registration.json', 'core.json']

    def test_str(self):
        """Test alt name representation."""
        self.assertEqual(str(AltName.objects.get(pk=1)),
                         'Manga One')


class IssueTestCase(TestCase):
    fixtures = ['registration.json', 'core.json']

    def test_is_sent(self):
        """Test if an issue was sent to an user."""
        # The fixture have one issue sent to both users. For user 1
        # was a success, but not for user 2.
        #
        # There is also, for user 1, a issue send via the third
        # subscription, that is deleted.
        user1 = UserProfile.objects.get(pk=1).user
        user2 = UserProfile.objects.get(pk=2).user

        issue_sent = Issue.objects.get(name='manga 1 issue 1')
        for issue in Issue.objects.all():
            if issue == issue_sent:
                self.assertTrue(issue.is_sent(user1))
                self.assertFalse(issue.is_sent(user2))
            else:
                self.assertFalse(issue.is_sent(user1))
                self.assertFalse(issue.is_sent(user2))

    def test_history(self):
        """Test the history of an issue."""
        # Read `test_is_sent` for a description of the fixture.
        user1 = UserProfile.objects.get(pk=1).user
        user2 = UserProfile.objects.get(pk=2).user

        issue_sent = Issue.objects.get(name='manga 1 issue 1')
        for issue in Issue.objects.all():
            if issue == issue_sent:
                self.assertEqual(len(issue.history(user1)), 1)
                self.assertEqual(len(issue.history(user2)), 1)
            else:
                self.assertEqual(len(issue.history(user1)), 0)
                self.assertEqual(len(issue.history(user2)), 0)


class SubscriptionTestCase(TestCase):
    fixtures = ['registration.json', 'core.json']

    def test_subscription_manager(self):
        """Test the subscription manager."""
        # There are six subscriptions, three for each user, and each
        # with a different state (active, paused, deleted)
        #
        # The subsctription manager are expected to filter deleted
        # instances.
        self.assertEqual(Subscription.objects.count(), 4)
        self.assertEqual(Subscription.all_objects.count(), 6)

    def test_latests(self):
        """Test the recovery of updated subscriptions."""
        # There are six subscriptions, three for each user, and each
        # with a different state (active, paused, deleted)
        for subs in Subscription.all_objects.order_by('pk'):
            issue = subs.manga.issue_set.first()
            subs.add_sent(issue)

        # Check that deleted subscriptions are not included
        rqs = Subscription.objects.latests()
        self.assertEqual(len(list(rqs)), 4)
        self.assertEqual(Subscription.all_objects.count(), 6)

        # Now the most up-to-dated subscription is the one with higher
        # `pk`.
        ids = [s.id for s in Subscription.objects.latests()]
        self.assertEqual(ids, sorted(ids, reverse=True))

    def test_str(self):
        """Test subscription representation"""
        self.assertEqual(str(Subscription.objects.get(pk=1)),
                         'Manga 1 (4 per day)')
