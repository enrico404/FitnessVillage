
from django.test import TestCase, Client
from django.urls import reverse
from .forms import CourseInsertForm
from django.utils import timezone
import datetime
from main_page.models import Sala
from django.contrib .messages import get_messages

class InsertCourseTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.insertUrl = reverse('courseManager:insert', args=['box'])

    def test_insertCourse_with_blank_data(self):
        response = self.client.get(self.insertUrl)
        form_data = {
            'data': '',
            'capienza': 0,
            'ora_inizio': '',
            'ora_fine': '',
            'posti_prenotati': 0,
            'sala': ''
        }
        test_form = CourseInsertForm(data=form_data)
        self.assertFalse(test_form.is_valid())

    def test_insertCourse_with_negative_data(self):
        response = self.client.get(self.insertUrl)
        sala = Sala.objects.create(num=1, cap_max=10)
        form_data = {
            'data': str(timezone.now()),
            'capienza': -10,
            'ora_inizio': str(timezone.now()),
            'ora_fine': str(timezone.now()),
            'posti_prenotati': -10,
            'sala': sala
        }
        test_form = CourseInsertForm(data=form_data)
        self.assertFalse(test_form.is_valid())


class courseDetailTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.loadUrl = reverse('courseManager:courseDetail', args=['prova'])

    def test_non_existing_course(self):
        response = self.client.get(self.loadUrl)
        self.assertEqual(response.status_code, 404)

