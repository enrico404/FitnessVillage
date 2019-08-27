
from django.test import TestCase, Client
from django.urls import reverse
from .forms import CourseInsertForm
from django.utils import timezone
import datetime
from main_page.models import Sala
from django.contrib .messages import get_messages
from django.contrib.auth.models import Group, User
from main_page.models import Corso

class CourseTests(TestCase):

    def setUp(self):
        self.client = Client()
        testUser, created1 = User.objects.get_or_create(username='testUser')
        self.insertUrl = reverse('courseManager:insert', args=['box'])
        testGroup, created3 = Group.objects.get_or_create(name='Operators')
        if created1:
            testUser.set_password('testUser123')
            testUser.save()
            testUser.groups.add(testGroup)
        self.client.login(username='testUser', password='testUser123')
        self.loadUrl = reverse('courseManager:courseDetail', args=['prova'])
        self.loadUrl2 = reverse('courseManager:courseDetail', args=['box'])

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
            'data': timezone.now(),
            'capienza': -10,
            'ora_inizio': datetime.time(00, 00),
            'ora_fine': datetime.time(00, 00),
            'posti_prenotati': -10,
            'sala': sala
        }
        test_form = CourseInsertForm(data=form_data)
        self.assertFalse(test_form.is_valid())

    def test_non_existing_course(self):
        response = self.client.get(self.loadUrl)
        self.assertEqual(response.status_code, 404)

    def test_existing_course(self):
        response = self.client.get(self.loadUrl2)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'courseManager/detail.html')


class PrenotazioneTests(TestCase):
    def setUp(self):
        self.client = Client()
        testUser, created1 = User.objects.get_or_create(username='testUser')
        self.nomeCorso = 'box'
        testGroup, created3 = Group.objects.get_or_create(name='Common')
        if created1:
            testUser.set_password('testUser123')
            testUser.save()
            testUser.groups.add(testGroup)

        operator, created = User.objects.get_or_create(username='operator')
        groupOp, created2 = Group.objects.get_or_create(name='Operators')
        if created:
            operator.set_password('operator123')
            operator.save()
            operator.groups.add(groupOp)

        self.insertUrl = reverse('courseManager:insert', args=[self.nomeCorso])
        self.sala = Sala(id=1, cap_max=10, num=1)
        self.sala.save()

        self.corso = Corso(nome=self.nomeCorso, data=timezone.now(), operatore=operator, cap=10, sala=self.sala,
                      ora_inizio=datetime.time(00, 00), ora_fine=datetime.time(00, 00), posti_prenotati=0)
        self.corso.save()

        self.prenUrl = reverse('courseManager:prenotazione', args=[self.corso.id])

    def test_prenotazione_operatore(self):
        self.client.login(username='operator', password='operator123')
        response = self.client.get(self.prenUrl)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Sei un operatore, non puoi prenotarti ad un corso!')

        self.client.logout()

    def test_prenotazione_user(self):
        self.client.login(username='testUser', password='testUser123')
        response = self.client.get(self.prenUrl)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Prenotato con successo!')

        self.client.logout()
