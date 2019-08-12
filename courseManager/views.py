from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import timezone
from main_page.models import Corso

@login_required
def courseDetail(request, nomeCorso):
    course_set = Corso.objects.filter(data__gte=timezone.now(), nome__exact=nomeCorso).order_by('data')
    return render(request, 'courseManager/detail.html', {'nomeCorso': nomeCorso, 'course_set': course_set})
