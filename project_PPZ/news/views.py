from django.http import HttpResponse

def index(request):
    return HttpResponse("Привіт із додатку news! Це мій проект з ППЗ")
