
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import Group, User
from .models import Messaggio
from django.utils import timezone
from django.contrib .messages import get_messages


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

        self.msg = Messaggio(userMittente=testUser, userDestinatario=testUser2, data_ora=timezone.now(), text='test')
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

        msg = Messaggio(userMittente=testUser, userDestinatario=testUser2, data_ora=timezone.now(), text='test')
        msg.save()
        self.msgUrl = reverse('main_page:rispondi', args=[msg.pk])

    def test_invio_messaggio(self):
        response = self.client.post(self.msgUrl, data={'form': {'data': timezone.now(), 'messaggio':'prova'}})
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Messaggio inviato con successo!')