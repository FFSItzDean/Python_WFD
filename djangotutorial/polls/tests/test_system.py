from django.test import SimpleTestCase, TransactionTestCase, tag
from polls.models import Question
from django.utils import timezone

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
