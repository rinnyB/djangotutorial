import datetime

from django.test import TestCase
from django.utils import timezone

from .models import Question


class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions
        with publication_date in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(publication_date=time)

        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for question
        with publication_date is within last day.
        """
        time = timezone.now() - datetime.timedelta(hours=12,
                                                   minutes=13,
                                                   seconds=14)
        recent_question = Question(publication_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for question
        that has publication_date older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(publication_date=time)
        self.assertIs(old_question.was_published_recently(), False)
