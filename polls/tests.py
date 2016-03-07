from django.test import TestCase

from .models import Question

import datetime
from django.utils import timezone

from django.core.urlresolvers import reverse 

class QuestionMethodTests(TestCase):

    def test_was_publishedf_recently_with_future_question(self):
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertEqual(future_question.was_published_in_last_7_days(), False)

    def test_was_published_recently_with_recent_question(self):
        time = timezone.now() - datetime.timedelta(hours=1)
        recent_question = Question(pub_date=time)
        self.assertEqual(recent_question.was_published_in_last_7_days(), True)

def create_question(question_text, days):
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)

class QuestionViewTests(TestCase):
    def test_index_view_with_no_questions(self):
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "You haven't uploaded any question yet.")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])

    def test_index_view_with_a_past_question(self):
        create_question(question_text="Past question?", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question?>']
        )

    def test_index_view_with_a_future_question(self):
        create_question(question_text="Future question?", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "You haven't uploaded any question yet.", status_code=200)
        self.assertQuerysetEqual(response.context["latest_question_list"], [])

    def test_index_view_with_future_question_and_past_question(self):
        create_question(question_text="Past question?", days=-30)
        create_question(question_text="Future question?", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question?>']
        )

    def test_index_view_with_two_past_questions(self):
        create_question(question_text="Past question 1?", days=-30)
        create_question(question_text="Past question 2?", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'],
            ['<Question: Past question 2?>','<Question: Past question 1?>'])

class QuestionIndexDetailTests(TestCase):
    def test_detail_view_with_a_past_question(self):
        past_question = create_question(question_text="Past question?", days=-5)
        response = self.client.get(reverse('polls:detail', args=(past_question.id,)))
        self.assertContains(response, past_question.question_text, status_code=200)
