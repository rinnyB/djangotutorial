"""Tests for polls app."""

import datetime

from django.test import TestCase
from django.urls import reverse
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


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        If no questions exist, an appropriate message is displayed
        """
        resp = self.client.get(reverse("polls:index"))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "No polls are available.")
        self.assertQuerysetEqual(resp.context["latest_question_list"], [])

    def test_past_question(self):
        """
        Question with a publication_date in the past are displayed
        on the index page.
        """
        create_question(question_text="Past Question", days=-30)
        resp = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            resp.context["latest_question_list"],
            ["<Question: Past Question>"])

    def test_future_question(self):
        """
        Questions with publication_date in the future
        are NOT displayed on the index page.
        """
        create_question(question_text="Future_question", days=30)
        resp = self.client.get(reverse("polls:index"))
        self.assertContains(resp, "No polls are available.")
        self.assertQuerysetEqual(resp.context["latest_question_list"], [])

    def test_future_and_past_questions(self):
        """
        Questions with publication_date in the future are NOT displayed,
        questions with publication_date in the past are displayed
        """
        create_question(question_text="Future_question", days=30)
        create_question(question_text="Past Question", days=-30)
        resp = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            resp.context["latest_question_list"],
            ["<Question: Past Question>"])

    def test_multiple_past_questions(self):
        """
        Questions index may display multiple questions
        """
        # create 10 questions
        for i in range(1, 11):
            create_question(question_text="Past question {}".format(i),
                            days=-i)
        resp = self.client.get(reverse("polls:index"))
        # note, that we're showing only 5 tests on the index page
        correct = [
            '<Question: Past question {}>'.format(i) for i in range(1, 6)]
        self.assertQuerysetEqual(resp.context['latest_question_list'], correct)


def create_question(question_text, days):
    """
    Create a question with `question_text`
    and published with `days` offset to now
    (negative for questions published,
    positive for questions yet to be published)
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text,
                                   publication_date=time)


class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """
        The detail view of a question with publication_date
        in the future returns 404.
        """
        future_question = create_question(question_text="Future question.",
                                          days=5)
        url = reverse("polls:detail", args=(future_question.id,))
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 404)
    
    def test_past_question(self):
        """
        The detail view of a question with a publication_date in the past
        displays the question text.
        """
        past_question = create_question(question_text="Past Question.",
                                        days=-5)
        url = reverse("polls:detail", args=(past_question.id,))
        resp = self.client.get(url)
        self.assertContains(resp, past_question.question_text)
