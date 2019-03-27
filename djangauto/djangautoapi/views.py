from django.http import HttpResponse

def index(request):
    return HttpResponse("You're at the cars index.")

def models(request):
    return HttpResponse("You're at the models index")