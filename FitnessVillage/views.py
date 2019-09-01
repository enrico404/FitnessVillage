from django.http import HttpResponseRedirect


def main_page(request):
    """
    Prima funzione che viene chiamata, redireziona alla main page
    :param request:
    :return:
    """
    return HttpResponseRedirect('/main_page/')

