from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import logout
from .models import User, Messaggio
from .forms import ContactForm
from django.contrib import messages
from django.db.models import Q


import random

def welcome(request):
    # flag che indica se sono presenti oppure no nuovi messaggi nella casella di posta
    new_messages = False
    if request.user.is_authenticated:
        messaggi = Messaggio.objects.filter(userDestinatario=request.user)
        for msg in messaggi:
            if msg.letto == False:
                new_messages = True
    return render(request, 'main_page/main_page.html', {'new_messages':new_messages})

def corso(request, nomeCorso):
    url = '/courseManager/'+nomeCorso
    return HttpResponseRedirect(url)

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

@login_required
def login(request):
    return HttpResponseRedirect('/')

@login_required
def assistenza(request):
    operator_list = User.objects.filter(groups__name='Operators')
    num = random.randint(0, len(operator_list)-1)
    random_operator = operator_list[num]
    form = ContactForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            mittente = request.user
            destinatario = random_operator
            data = form.cleaned_data['data']
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
    messaggi = Messaggio.objects.filter(Q(userDestinatario=request.user)).order_by('data_ora').reverse()
    return render(request, 'main_page/messaggi.html', {'messaggi': messaggi})


def rispondi(request, messageID):
    form = ContactForm(request.POST)
    message = Messaggio.objects.get(id=messageID)
    message.letto = True
    message.save()
    form = ContactForm(request.POST)
    mittente = message.userDestinatario
    destinatario = message.userMittente
    if request.method == 'POST':
        if form.is_valid():
            data = form.cleaned_data['data']
            testo = form.cleaned_data['messaggio']
            messaggio = Messaggio(userMittente=mittente, userDestinatario=destinatario, data_ora=data, text=testo)
            messaggio.save()
            messages.add_message(request, messages.SUCCESS, 'Messaggio inviato con successo!')
            return HttpResponseRedirect('/')
    else:
        form = ContactForm()
        return render(request, 'main_page/response.html', {'form': form, 'mittente':mittente, 'destinatario':destinatario, 'message':message})