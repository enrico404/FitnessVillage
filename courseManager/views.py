from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import timezone
from main_page.models import Corso, Prenota
from django.shortcuts import HttpResponseRedirect
from django.contrib import messages
from .forms import CourseInsertForm

@login_required
def courseDetail(request, nomeCorso):
    course_set = Corso.objects.filter(data__gte=timezone.now(), nome__exact=nomeCorso).order_by('data')
    posti_disponibili = []
    for course in course_set:
        nposti = course.cap - course.posti_prenotati
        posti_disponibili.append(nposti)
    return render(request, 'courseManager/detail.html', {'nomeCorso': nomeCorso, 'course_set': course_set, 'posti_disponibili': posti_disponibili })

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
            nome = form.cleaned_data['nome']
            data = form.cleaned_data['data']
            capienza = form.cleaned_data['capienza']
            posti_prenotati = form.cleaned_data['posti_prenotati']
            operatore = form.cleaned_data['operatore']
            newCourse = Corso(nome=nome, data=data, cap=capienza, )

            return HttpResponseRedirect('/courseManager/'+nomeCorso)
    else:
        form = CourseInsertForm()
        return render(request, 'courseManager/insertCourse.html', {'nomeCorso': nomeCorso, 'form':form})
