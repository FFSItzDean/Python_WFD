import datetime
from django.test import TestCase, SimpleTestCase, TransactionTestCase, LiveServerTestCase, RequestFactory, tag
from django.utils import timezone
from django.urls import reverse
from .models import Question, Choice
from .views import IndexView

class QuestionRequestFactoryTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    @tag('fast')
    def test_index_view_status(self):
        request = self.factory.get("/")
        response = IndexView.as_view()(request)
        self.assertEqual(response.status_code, 200)

class QuestionModelTests(TestCase):
    @tag('logic', 'fast')
    def test_was_published_recently_with_future_question(self):
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

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

class PollsSimpleTests(SimpleTestCase):
    def test_admin_login_template(self):
        response = self.client.get('/admin/login/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "admin/login.html")

class QuestionTransactionTests(TransactionTestCase):
    @tag('database')
    def test_database_integrity(self):
        q = Question.objects.create(question_text="Transaction?", pub_date=timezone.now())
        self.assertEqual(Question.objects.count(), 1)

class PollsLiveTests(LiveServerTestCase):
    def test_live_server_index_check(self):
        response = self.client.get(self.live_server_url + reverse('polls:index'))
        self.assertEqual(response.status_code, 200)