from django.http import HttpResponseRedirect

def main_page(request):
    return HttpResponseRedirect('/main_page/')

