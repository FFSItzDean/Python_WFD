from django.test import TestCase, RequestFactory, tag
from django.urls import reverse
from polls.models import Question, Choice
from polls.views import IndexView
from django.utils import timezone

class QuestionRequestFactoryTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    @tag('fast')
    def test_index_view_status(self):
        request = self.factory.get("/")
        response = IndexView.as_view()(request)
        self.assertEqual(response.status_code, 200)

class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["latest_question_list"], [])

    def test_voting_redirect(self):
        question = Question.objects.create(question_text="Vote Test", pub_date=timezone.now())
        choice = Choice.objects.create(question=question, choice_text="Option 1", votes=0)
        response = self.client.post(
            reverse("polls:vote", args=(question.id,)), 
            {"choice": choice.id}, 
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.redirect_chain) > 0)
