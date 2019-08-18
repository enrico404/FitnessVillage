from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import timezone
from main_page.models import Corso, Prenota
from django.shortcuts import HttpResponseRedirect
from django.contrib import messages
from .forms import CourseInsertForm
from django.db.models import Q
import datetime

@login_required
def courseDetail(request, nomeCorso):
    course_set_tmp = Corso.objects.filter(data__gte=timezone.now(), nome__exact=nomeCorso).order_by('data', 'ora_inizio')
    course_set = []
    for course in course_set_tmp:
        if course.data == datetime.date.today():
            if course.ora_fine < datetime.datetime.now().time():
                continue
        course_set.append(course)

    posti_disponibili = []
    for course in course_set:
        nposti = course.cap - course.posti_prenotati
        posti_disponibili.append(nposti)

    prenotazioni_tmp = Prenota.objects.filter(user=request.user)
    prenotazioni = []
    for pren in prenotazioni_tmp:
        prenotazioni.append(pren.corso.id)

    return render(request, 'courseManager/detail.html', {'nomeCorso': nomeCorso, 'course_set': course_set, 'posti_disponibili': posti_disponibili, 'prenotazioni':prenotazioni})

@login_required
def prenotazione(request, corsoID):
    corso = Corso.objects.get(pk=corsoID)
    user = request.user
    CourseName = corso.nome
    prenotazione = Prenota(user=user, corso=corso)
    #flag per cedere se esiste la prenotazione
    pren = Prenota.objects.filter(user=user, corso=corso).exists()
    operator = user.groups.filter(name='Operators').exists()

    if corso.posti_prenotati <= corso.cap and not operator and not pren:
        corso.posti_prenotati += 1
        corso.save()
        prenotazione.save()
        return HttpResponseRedirect('/courseManager/'+CourseName)

    if pren:
        messages.add_message(request, messages.ERROR, 'Sei già prenotato al corso!')
    elif operator:
        messages.add_message(request, messages.ERROR, 'Sei un operatore, non puoi prenotarti ad un corso!')

    return HttpResponseRedirect('/courseManager/'+CourseName)


@login_required
def insert(request, nomeCorso):
    form = CourseInsertForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            nome = nomeCorso
            data = form.cleaned_data['data']
            capienza = form.cleaned_data['capienza']
            posti_prenotati = form.cleaned_data['posti_prenotati']
            operatore = request.user
            sala = form.cleaned_data['sala']
            ora_inizio = form.cleaned_data['ora_inizio']
            ora_fine = form.cleaned_data['ora_fine']
            newCourse = Corso(nome=nome, data=data, operatore=operatore, cap=capienza, sala=sala, ora_inizio=ora_inizio, ora_fine=ora_fine, posti_prenotati=posti_prenotati)
            #se il corso non esiste già
            corsi_del_giorno = Corso.objects.filter(Q(nome=nome), Q(data__year=data.year), Q(data__month=data.month), Q(data__day=data.day), Q(sala=sala))
            #chechk che la sala non sia occupata in quell'ora, se è occupata esco
            for corso in corsi_del_giorno:
                if not (corso.ora_fine <= ora_inizio or corso.ora_inizio >= ora_fine):
                    messages.add_message(request, messages.ERROR, 'La sala è già occupata da un altro corso!')
                    return HttpResponseRedirect('/courseManager/' + nomeCorso)
            if sala.cap_max >= newCourse.cap:
                newCourse.save()
                messages.add_message(request, messages.SUCCESS, 'Corso inserito con successo!')
                return HttpResponseRedirect('/courseManager/' + nomeCorso)
            else:
                messages.add_message(request, messages.ERROR, "La capienza del corso supera la capienza massima della sala!")
        messages.add_message(request, messages.ERROR, "Errore nell'inserimento del corso!")
        return HttpResponseRedirect('/courseManager/' + nomeCorso)
    else:
        form = CourseInsertForm()
        return render(request, 'courseManager/insertCourse.html', {'nomeCorso': nomeCorso, 'form':form})


@login_required
def cancella(request, corsoID, nomeCorso):
    ''' il corso in realtà non si cancella dal database, viene cambiato solo il flag di cancellazione '''
    corso = Corso.objects.get(pk=corsoID)
    corso.cancellato = True
    # cambio data così non dà fastidio all'inserimento
    corso.data = datetime.date(3000, 12, 12)
    corso.save()
    return HttpResponseRedirect('/courseManager/' + nomeCorso)