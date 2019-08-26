from django.test import TestCase
from django.test import TestCase, Client
from django.urls import reverse

class MainPage_view_Tests(TestCase):
    def setUp(self):
        self.client = Client()
        self.corso = reverse('main_page:corso', args=['prova'])
    def test_click_non_ex_course(self):
        response = self.client.get(self.corso)
        self.assertRedirects(response, '/courseManager/prova', status_code=302, target_status_code=301)
        self.assertEqual(self.corso, '/main_page/corso/prova')