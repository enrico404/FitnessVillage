from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import timezone
from main_page.models import Corso, Prenota, ListaAttesa, Inserito
from django.shortcuts import HttpResponseRedirect, HttpResponse, Http404
from django.contrib import messages
from .forms import CourseInsertForm
from django.db.models import Q
from django.http import Http404
import datetime

@login_required
def courseDetail(request, nomeCorso):
    listaCorsi = ['box','aerobica','mma','yoga','crossfit','pilates']
    course_set_tmp = Corso.objects.filter(data__gte=timezone.now(), nome__exact=nomeCorso).order_by('data', 'ora_inizio')
    course_set = []
    for course in course_set_tmp:
        if not course.scaduto():
            course_set.append(course)

    posti_disponibili = []
    for course in course_set:
        nposti = course.cap - course.posti_prenotati
        posti_disponibili.append(nposti)

    prenotazioni_tmp = Prenota.objects.filter(user=request.user)
    prenotazioni = []
    for pren in prenotazioni_tmp:
        prenotazioni.append(pren.corso.id)

    #lista di valori booleani che indica se una prenotazione è stata cancellata oppure no
    prenotazioniCancellate = []
    for pren in prenotazioni_tmp:
        prenotazioniCancellate.append(pren)
    if nomeCorso in listaCorsi:
        return render(request, 'courseManager/detail.html', {'nomeCorso': nomeCorso, 'course_set': course_set, 'posti_disponibili': posti_disponibili, 'prenotazioni':prenotazioni, 'prenotazioniCancellate':prenotazioniCancellate})
    else:
        raise Http404

@login_required
def prenotazione(request, corsoID):
    corso = Corso.objects.get(id=corsoID)
    user = request.user
    CourseName = corso.nome
    prenotazione = Prenota(user=user, corso=corso, cancellato=False)
    #flag per vedere se esiste la prenotazione
    pren = Prenota.objects.filter(user=user, corso=corso)

    #se l'utente appartiene al gruppo degli operatori vale true
    operator = user.groups.filter(name='Operators').exists()

    if corso.posti_prenotati <= corso.cap and not operator and not pren:
        corso.posti_prenotati += 1
        corso.save()
        prenotazione.save()
        messages.add_message(request, messages.SUCCESS, 'Prenotato con successo!')
        return HttpResponseRedirect('/courseManager/'+CourseName)

    if pren and pren[0].cancellato == False:
        messages.add_message(request, messages.ERROR, 'Sei già prenotato al corso!')
    elif operator:
        messages.add_message(request, messages.ERROR, 'Sei un operatore, non puoi prenotarti ad un corso!')
    elif pren and pren[0].cancellato == True:
        pren[0].cancellato = False
        corso.posti_prenotati += 1
        corso.save()
        pren[0].save()
        messages.add_message(request, messages.SUCCESS, 'Prenotato con successo!')
    return HttpResponseRedirect('/courseManager/'+CourseName)

@login_required
def listaAttesa(request, corsoID, nomeCorso):
    """
    :param request:
    :param corsoID:
    :param nomeCorso:
    :return: s

    funzione per l'inserimento in lista di attesa di un utente in un corso
    """
    corso = Corso.objects.get(pk=corsoID)
    lista = ListaAttesa.objects.get(corso=corso)
    insLista = Inserito(user=request.user, listaAttesa=lista)

    operator = request.user.groups.filter(name='Operators').exists()
    pren = Prenota.objects.filter(user=request.user, corso=corso)
    if operator:
        messages.add_message(request, messages.ERROR, 'Sei un operatore, non puoi metterti in lista di attesa in un corso!')
        return HttpResponseRedirect('/courseManager/' + nomeCorso)
    if pren and pren[0].cancellato == False:
        messages.add_message(request, messages.ERROR,
                             'Sei già prenotato al corso!')
        return HttpResponseRedirect('/courseManager/' + nomeCorso)
    checkExists = Inserito.objects.filter(user=request.user, listaAttesa=lista, cancellato=False).exists()
    if not checkExists:
        insLista.save()
        messages.add_message(request, messages.SUCCESS, 'Ti sei inserito in lista di attesa per il corso di '+ nomeCorso)
        return HttpResponseRedirect('/courseManager/' + nomeCorso)
    else:
        messages.add_message(request, messages.ERROR, 'Sei già in lista di attesa!')
        return HttpResponseRedirect('/courseManager/' + nomeCorso)

@login_required
def cancellaPrenotazione(request, corsoID):
    corso = Corso.objects.get(pk=corsoID)
    CourseName = corso.nome
    prenotazione = Prenota.objects.get(user=request.user, corso=corso)
    #cancellazione della prenotazione
    corso.posti_prenotati = corso.posti_prenotati - 1
    prenotazione.cancellato = True
    #salvataggio nel db
    corso.save()
    prenotazione.save()

    return HttpResponseRedirect('/courseManager/' + CourseName)


@login_required
def insert(request, nomeCorso):
    form = CourseInsertForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            nome = nomeCorso
            data = form.cleaned_data['date']
            capienza = form.cleaned_data['capienza']
            posti_prenotati = form.cleaned_data['posti_prenotati']
            operatore = request.user
            sala = form.cleaned_data['sala']
            ora_inizio = form.cleaned_data['ora_inizio']
            ora_fine = form.cleaned_data['ora_fine']

            if capienza < posti_prenotati:
                messages.add_message(request, messages.ERROR, 'Il numero di posti prenotati non può essere maggiore della capienza del corso!')
                return HttpResponseRedirect('/courseManager/' + nomeCorso)

            newCourse = Corso(nome=nome, data=data, operatore=operatore, cap=capienza, sala=sala, ora_inizio=ora_inizio, ora_fine=ora_fine, posti_prenotati=posti_prenotati)
            #se il corso non esiste già
            corsi_del_giorno = Corso.objects.filter(Q(data__year=data.year), Q(data__month=data.month), Q(data__day=data.day), Q(sala=sala), Q(cancellato=False))
            #check che la sala non sia occupata in quell'ora, se è occupata esco
            for corso in corsi_del_giorno:
                if not (corso.ora_fine <= ora_inizio or corso.ora_inizio >= ora_fine):
                    msg = 'La sala è già occupata da un altro corso dalle '+ str(corso.ora_inizio) + ' alle '+ str(corso.ora_fine)
                    messages.add_message(request, messages.ERROR, msg)
                    return HttpResponseRedirect('/courseManager/' + nomeCorso+ '/insertCourse')
            if sala.cap_max >= newCourse.cap:
                newCourse.save()
                messages.add_message(request, messages.SUCCESS, 'Corso inserito con successo!')
                #creo lista di attesa per quel corso
                listaAttesa = ListaAttesa(corso=newCourse)
                listaAttesa.save()
                return HttpResponseRedirect('/courseManager/' + nomeCorso)
            else:
                msg = "La capienza del corso supera la capienza massima della sala! (max "+ str(sala.cap_max)+ ' posti)'
                messages.add_message(request, messages.ERROR, msg)
        messages.add_message(request, messages.ERROR, "Errore nell'inserimento del corso!")
        return HttpResponseRedirect('/courseManager/' + nomeCorso)
    else:
        form = CourseInsertForm()
        return render(request, 'courseManager/insertCourse.html', {'nomeCorso': nomeCorso, 'form':form})


@login_required
def cancella(request, corsoID, nomeCorso):
    """
    :param request:
    :param corsoID:
    :param nomeCorso:
    :return:

    funzione per la cancellazione del corso
    """
    corso = Corso.objects.get(pk=corsoID)
    corso.cancellato = True
    # cambio data così non dà fastidio all'inserimento
    corso.data = datetime.date(3000, 12, 12)
    corso.save()
    return HttpResponseRedirect('/courseManager/' + nomeCorso)





