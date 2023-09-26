from django.shortcuts import render, redirect, HttpResponse
from core.models import Evento

# Create your views here.
#def index(request):
#    return redirect('/agenda/')

def listaEventos(request):
    usuario = request.user
    evento = Evento.objects.all()
    data = {'eventos':evento}
    return render (request, 'agenda.html', data)