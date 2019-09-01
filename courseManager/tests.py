
from django.test import TestCase, Client
from django.urls import reverse
from .forms import CourseInsertForm
import datetime
from main_page.models import Sala
from django.contrib .messages import get_messages
from django.contrib.auth.models import Group, User
from main_page.models import Corso, ListaAttesa, Inserito

class CourseTests(TestCase):
    """
    test case relativi alla gestione dei corsi
    """
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
        # test per verificare il comportamente all'inserimento di un corso vuoto
        response = self.client.get(self.insertUrl)
        sala = Sala.objects.create(cap_max=10)
        form_data = {
            'date': datetime.datetime.today(),
            'capienza': 0,
            'ora_inizio': datetime.time(00,00),
            'ora_fine': datetime.time(00,00),
            'posti_prenotati': 0,
            'sala': 0
        }
        test_form = CourseInsertForm(form_data)
        self.assertFalse(test_form.is_valid())

    def test_insertCourse_with_negative_data(self):
        # test per verificare il comportamento all'inserimento di un corso con valori negativi
        response = self.client.get(self.insertUrl)
        sala = Sala.objects.create(cap_max=10)
        form_data = {
            'date': datetime.datetime.today(),
            'capienza': -10,
            'ora_inizio': datetime.time(00, 00),
            'ora_fine': datetime.time(00, 00),
            'posti_prenotati': -10,
            'sala': sala.pk
        }
        test_form = CourseInsertForm(form_data)
        self.assertFalse(test_form.is_valid())

    def test_non_existing_course(self):
        # test per verificare il comportamento al caricamento di un corso non presente nella palestra
        response = self.client.get(self.loadUrl)
        self.assertEqual(response.status_code, 404)

    def test_existing_course(self):
        # test di verifica del comportamento al click di un corso esistente
        response = self.client.get(self.loadUrl2)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'courseManager/detail.html')


class PrenotazioneTests(TestCase):
    """
    Test case relativi alla funzione di prenotazione dei corsi
    """
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
        self.sala = Sala(id=1, cap_max=10)
        self.sala.save()

        self.corso = Corso(nome=self.nomeCorso, data=datetime.datetime.today(), operatore=operator, cap=10, sala=self.sala,
                      ora_inizio=datetime.time(00, 00), ora_fine=datetime.time(00, 00), posti_prenotati=0)
        self.corso.save()

        self.listaAttesa = ListaAttesa(id=1, corso=self.corso)

        self.listaAttesa.save()


        self.listaAttesaUrl = reverse('courseManager:listaAttesa', args=[self.corso.id, self.nomeCorso])
        self.prenUrl = reverse('courseManager:prenotazione', args=[self.corso.id])

    def test_prenotazione_operatore(self):
        # test per vericare comportamento alla prenotazione di un operatore ad un corso, mon deve essere possibile
        self.client.login(username='operator', password='operator123')
        response = self.client.get(self.prenUrl)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Sei un operatore, non puoi prenotarti ad un corso!')

        self.client.logout()

    def test_prenotazione_user(self):
        # test per verificare compportamento prenotazione di un utente ad un corso
        self.client.login(username='testUser', password='testUser123')
        response = self.client.get(self.prenUrl)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Prenotato con successo!')
        self.client.logout()

    def test_lista_attesa_operatore(self):
        # test per verificare comportamento all'inserimento in lista di attesa di un operatore
        self.client.login(username='operator', password='operator123')
        response = self.client.get(self.listaAttesaUrl)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Sei un operatore, non puoi metterti in lista di attesa in un corso!')
        self.client.logout()

    def test_lista_attesa_user(self):
        # test per verificare comportamento all'inserimento in lista di attesa di un utente
        self.client.login(username='testUser', password='testUser123')
        response = self.client.get(self.listaAttesaUrl)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Ti sei inserito in lista di attesa per il corso di '+ self.nomeCorso)
        self.client.logout()
        user = User.objects.get(username='testUser')
        inserimento = Inserito.objects.get(user=user, listaAttesa=self.listaAttesa)
        self.assertTrue(inserimento)

    def test_insLista_due_volte(self):
        # test per verificare comportamento se un utwente prova ad inserirsi due volte nella stessa lista di attesa
        self.client.login(username='testUser', password='testUser123')
        response = self.client.get(self.listaAttesaUrl)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Ti sei inserito in lista di attesa per il corso di ' + self.nomeCorso)
        user = User.objects.get(username='testUser')
        inserimento = Inserito.objects.get(user=user, listaAttesa=self.listaAttesa)
        self.assertTrue(inserimento)
        #second insert
        response = self.client.get(self.listaAttesaUrl)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 2)
        self.assertEqual(str(messages[1]), 'Sei già in lista di attesa!')
        self.client.logout()