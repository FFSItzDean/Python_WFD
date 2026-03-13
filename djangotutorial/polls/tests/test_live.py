from django.test import LiveServerTestCase
from django.urls import reverse

class PollsLiveTests(LiveServerTestCase):
    def test_live_server_index_check(self):
        response = self.client.get(self.live_server_url + reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
