from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import logout


def welcome(request):
    return render(request, 'main_page/main_page.html')

def corso(request, nomeCorso):
    url = '/courseManager/'+nomeCorso
    return HttpResponseRedirect(url)

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

@login_required
def login(request):
    return HttpResponseRedirect('/')