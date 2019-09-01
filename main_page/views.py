from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import logout
from .models import User, Messaggio, Prenota, ListaAttesa, Inserito
from .forms import ContactForm
from django.contrib import messages
from django.db.models import Q
import random
import datetime
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group


def controlList(user):
    """
    funzione che manda le notifiche agli utenti, si attiva non appena l'utente carica la home
    :param user:
    :return:
    """
    insListe = Inserito.objects.filter(user=user, cancellato=False).select_related('listaAttesa')
    for l in insListe:
        numPosti = l.listaAttesa.corso.cap - l.listaAttesa.corso.posti_prenotati
        if numPosti > 0:
            testo = "Si è liberato un posto per il corso "+l.listaAttesa.corso.nome+ " che si tiene il "+ str(l.listaAttesa.corso.data) + " alle "+ str(l.listaAttesa.corso.ora_inizio)
            noreply = User.objects.get(username='noreply')
            notifica = Messaggio(userMittente=noreply, userDestinatario=user, data_ora=datetime.datetime.today(), text=testo)
            checkEx = Messaggio.objects.filter(userMittente=noreply, userDestinatario=user, text=testo).exists()
            if not checkEx:
                notifica.save()
                changeListRecord = Inserito.objects.get(user=user, listaAttesa=l.listaAttesa)
                changeListRecord.cancellato = True
                changeListRecord.save()

def welcome(request):
    """
    funzione per il rendering della view relativa alla main page
    :param request:
    :return:
    """
    # flag che indica se sono presenti oppure no nuovi messaggi nella casella di posta
    new_messages = False
    if request.user.is_authenticated:
        # controllo le liste di attesa a cui è prenotato l'utente
        controlList(request.user)
        messaggi = Messaggio.objects.filter(userDestinatario=request.user)
        for msg in messaggi:
            if msg.letto == False:
                new_messages = True
    return render(request, 'main_page/main_page.html', {'new_messages':new_messages})

def corso(request, nomeCorso):
    """
    funzione per la redirezione al corso cliccato dall'utente
    :param request:
    :param nomeCorso:
    :return:
    """
    url = '/courseManager/'+nomeCorso
    return HttpResponseRedirect(url)

def logout_view(request):
    """
    funzione per gestire il logout dell'utente attualmente loggato
    :param request:
    :return:
    """
    logout(request)
    return HttpResponseRedirect('/')


@login_required
def login(request):
    """
    funzione per il rendering della view di login utente nel caso non abbia effettuato l'accesso
    :param request:
    :return:
    """
    return HttpResponseRedirect('/')

def registrati(request):
    """
    funzione per il rendering della view relativa alla registrazione utenti, si occupa anche del salvataggio di nuovi utenti
    :param request:
    :return:
    """
    form = UserCreationForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            login(request, user)
            my_group = Group.objects.get(name='Common')
            my_group.user_set.add(user)
            messages.add_message(request, messages.SUCCESS, 'Utente creato con successo!')
            return HttpResponseRedirect('/')
        else:
            for msg in form.error_messages:
                messages.add_message(request, messages.ERROR, form.error_messages[msg])
            HttpResponseRedirect('main_page/registration')
    form = UserCreationForm()
    return render(request, 'registration/registrati.html', {'form': form})

@login_required
def assistenza(request):
    """
    funzione per il rendering della view relativa alla pagina di assistenza clienti
    :param request:
    :return:
    """
    operator_list = User.objects.filter(groups__name='Operators')
    num = random.randint(0, len(operator_list)-1)
    random_operator = operator_list[num]
    form = ContactForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            mittente = request.user
            destinatario = random_operator
            data = form.cleaned_data['date']
            testo = form.cleaned_data['messaggio']
            messaggio = Messaggio(userMittente=mittente, userDestinatario=destinatario, data_ora=data, text=testo)
            messaggio.save()
            messages.add_message(request, messages.SUCCESS, 'Messaggio inviato con successo!')
            return HttpResponseRedirect('/')
    else:
        form = ContactForm()
        return render(request, 'main_page/contact.html', {'form': form, 'operator': random_operator})

@login_required
def messaggi(request):
    """
    funzione per il redering della view relativa al centro messaggi
    :param request:
    :return:
    """
    messaggi = Messaggio.objects.filter(Q(userDestinatario=request.user)).order_by('data_ora').reverse()
    return render(request, 'main_page/messaggi.html', {'messaggi': messaggi})

@login_required()
def rispondi(request, messageID):
    """
    funzione per la risposta ad un messaggio
    :param request:
    :param messageID:
    :return:
    """
    form = ContactForm(request.POST)
    message = Messaggio.objects.get(id=messageID)
    message.letto = True
    message.save()
    form = ContactForm(request.POST)
    mittente = message.userDestinatario
    destinatario = message.userMittente
    if request.method == 'POST':
        if form.is_valid():
            data = form.cleaned_data['date']
            testo = form.cleaned_data['messaggio']
            messaggio = Messaggio(userMittente=mittente, userDestinatario=destinatario, data_ora=data, text=testo)
            messaggio.save()
            messages.add_message(request, messages.SUCCESS, 'Messaggio inviato con successo!')
            return HttpResponseRedirect('/')
    else:
        form = ContactForm()
        return render(request, 'main_page/response.html', {'form': form, 'mittente':mittente, 'destinatario':destinatario, 'message':message})