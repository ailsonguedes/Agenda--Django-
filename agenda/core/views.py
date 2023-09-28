from django.contrib.auth.models import User
from django.shortcuts import render, redirect, HttpResponse
from core.models import Evento
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from datetime import datetime, timedelta
from django.http.response import Http404, JsonResponse

# Create your views here.
#def index(request):
#    return redirect('/agenda/')

def loginUser(request):
    return render (request, 'login.html')

def logoutUser(request):
    logout(request)
    return redirect ('/')

def submitLogin(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        usuario = authenticate(username=username, password=password)
        if usuario is not None:
            login (request, usuario)
            return redirect ('/') 
        else:
            messages.error(request, "usuário ou senha inválidos")
    return redirect ('/')

@login_required(login_url='/login/')
def listaEventos(request):
    usuario = request.user
    dataAtual = datetime.now() - timedelta(hours=1)
    evento = Evento.objects.filter(usuario=usuario,
                                   dataEvento__gt=dataAtual)
    data = {'eventos':evento}
    return render (request, 'agenda.html', data)

@login_required(login_url='/login/')
def evento(request):
    id_evento = request.GET.get('id')
    dados = {}
    if id_evento:
        dados['evento'] = Evento.objects.get(id=id_evento)
    return render (request, 'evento.html', dados)

@login_required(login_url='/login/')
def submitEvento(request):
    if request.POST:
        titulo = request.POST.get('titulo')
        dataEvento = request.POST.get('dataEvento')
        descricao = request.POST.get('descricao')
        usuario = request.user
        id_evento = request.POST.get('id_evento')
        
        if id_evento:
            evento = Evento.objects.get(id=id_evento)
            if evento.usuario == usuario:
                evento.titulo = titulo
                evento.dataEvento = dataEvento
                evento.descricao = descricao
                evento.save()
            #Evento.objects.filter(id=id_evento).update(titulo=titulo,
            #                                           dataEvento=dataEvento,
            #                                           descricao=descricao)
        else:
            Evento.objects.create(titulo=titulo, 
                              dataEvento=dataEvento, 
                              descricao=descricao,
                              usuario=usuario)
        
    return redirect ('/')

@login_required(login_url='/login/')
def deleteEvento(request, id_evento):
    usuario = request.user
    try:
        evento = Evento.objects.get(id=id_evento)
    except Exception:
        raise Http404()
    if usuario == evento.usuario:
        evento.delete()
    else:
        raise Http404()
    return redirect('/')

#@login_required(login_url='/login/')
def jsonListaEvento(request, id_usuario):
    usuario = User.objects.get(id=id_usuario)
    evento = Evento.objects.filter(usuario=usuario).values('id', 'titulo')
    return JsonResponse(list(evento), safe=False)