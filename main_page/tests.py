
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import Group, User
from .models import Messaggio, Corso, Sala
from django.contrib .messages import get_messages
import datetime
from .forms import ContactForm

class MainPage_view_Tests(TestCase):
    """ test suite per la view main_page """
    def setUp(self):
        self.client = Client()
        testUser, created1 = User.objects.get_or_create(username='testUser')
        testUser2, created2 = User.objects.get_or_create(username='testUser2')
        testGroup, created3 = Group.objects.get_or_create(name='Common')
        if created1:
            testUser.set_password('testUser123')
            testUser.save()
            testUser.groups.add(testGroup)

        if created2:
            testUser2.set_password('testUser2123')
            testUser2.save()
            testUser2.groups.add(testGroup)
        self.client.login(username='testUser', password='testUser123')

        self.welcomeUrl = reverse('main_page:welcome')
        self.contactUrl = reverse('main_page:assistenza')
        self.messaggiUrl = reverse('main_page:messaggi')

        self.msg = Messaggio(userMittente=testUser, userDestinatario=testUser2, data_ora=datetime.datetime.today(), text='test')
        self.msg.save()

        self.reponseUrl = reverse('main_page:rispondi', args=[self.msg.id])

    def test_welcome_page(self):
        response = self.client.get(self.welcomeUrl)
        self.assertTemplateUsed(response, 'main_page/main_page.html')
        self.assertEqual(response.status_code, 200)

    def test_contact_page(self):
        response = self.client.get(self.contactUrl)
        self.assertTemplateUsed(response, 'main_page/contact.html')
        self.assertEqual(response.status_code, 200)

    def test_messaggi_page(self):
        response = self.client.get(self.messaggiUrl)
        self.assertTemplateUsed(response, 'main_page/messaggi.html')
        self.assertEqual(response.status_code, 200)

    def test_response_page(self):
        response = self.client.get(self.reponseUrl)
        self.assertTemplateUsed(response, 'main_page/response.html')
        self.assertEqual(response.status_code, 200)

class MessageTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.testUser, created1 = User.objects.get_or_create(username='testUser')
        testUser2, created2 = User.objects.get_or_create(username='testUser2')
        testGroup, created3 = Group.objects.get_or_create(name='Common')
        if created1:
            self.testUser.set_password('testUser123')
            self.testUser.save()
            self.testUser.groups.add(testGroup)

        if created2:
            testUser2.set_password('testUser2123')
            testUser2.save()
            testUser2.groups.add(testGroup)
        self.client.login(username='testUser', password='testUser123')

        msg = Messaggio(id=1, userMittente=self.testUser, userDestinatario=testUser2, data_ora=datetime.datetime.today(), text='test')
        msg.save()
        self.msgUrl = reverse('main_page:rispondi', args=[msg.id])

    def test_invio_messaggio(self):
        form = ContactForm({'date': datetime.datetime.today(),'messaggio':'prova'})
        response = self.client.post(self.msgUrl, data=form.data)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Messaggio inviato con successo!')


class CorsoMethodTests(TestCase):
    """
    suite di test per l'entità corso del modello, va a testare i suoi metodi
    """

    def setUp(self):
        self.client = Client()
        self.testUser, created1 = User.objects.get_or_create(username='testUser')
        testGroup, created3 = Group.objects.get_or_create(name='Operators')
        if created1:
            self.testUser.set_password('testUser123')
            self.testUser.save()
            self.testUser.groups.add(testGroup)

        self.sala = Sala(id=1, cap_max=10)

    def test_scaduto_with_current_time(self):
        ora_inizio = datetime.datetime.now()
        ora_fine = datetime.datetime.now()
        data = datetime.date.today()
        corso = Corso(nome='box', data=data, operatore=self.testUser, cap=10, sala=self.sala, ora_inizio=ora_inizio.time(), ora_fine=ora_fine.time(), posti_prenotati=0)
        self.assertTrue(corso.scaduto())

    def test_scaduto_with_ora_inizio_mag_current_time(self):
        ora_inizio = datetime.datetime.now() + datetime.timedelta(hours=1)
        ora_fine = datetime.datetime.now() + datetime.timedelta(hours=2)
        data = datetime.date.today()
        corso = Corso(nome='box', data=data, operatore=self.testUser, cap=10, sala=self.sala, ora_inizio=ora_inizio.time(),
                      ora_fine=ora_fine.time(), posti_prenotati=0)
        self.assertFalse(corso.scaduto())

    def test_scaduto_with_ora_fine_min_current_time(self):
        ora_inizio = datetime.datetime.now() - datetime.timedelta(hours=3)
        ora_fine = datetime.datetime.now() - datetime.timedelta(hours=2)
        data =  datetime.date.today()
        corso = Corso(nome='box', data=data, operatore=self.testUser, cap=10, sala=self.sala, ora_inizio=ora_inizio.time(),
                      ora_fine=ora_fine.time(), posti_prenotati=0)
        self.assertTrue(corso.scaduto())

    def test_scaduto_with_old_data(self):
        ora_inizio = datetime.datetime.now()
        ora_fine = datetime.datetime.now()
        data = datetime.date.today() - datetime.timedelta(days=2)
        corso = Corso(nome='box', data=data, operatore=self.testUser, cap=10, sala=self.sala, ora_inizio=ora_inizio.time(),
                      ora_fine=ora_fine.time(), posti_prenotati=0)
        self.assertTrue(corso.scaduto())