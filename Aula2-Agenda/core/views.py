from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from core.models import Evento
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from datetime import datetime, timedelta
from django.http.response import Http404, JsonResponse

# Create your views here.

#def index (request):
#    return redirect('/agenda/')

def login_user(request):
    return render(request, 'login.html')

def logout_user(request):
    logout(request)
    return redirect('/')

def submit_login(request):
    if request.POST:
        username = request.POST.get('username') #recuperar o conteúdo do parâmetro 'username' na url submit_login
        password = request.POST.get('password')
        usuario = authenticate(username=username, password=password)
        if usuario is not None: #se o user ñ for vazio, é feito o login; e retornando ao índice '/'
            login(request, usuario)
            return redirect('/') #ao retornar p/ o índice ele vai passar pela validação do decorador required...
        else:
            messages.error(request, "Usuário ou senha inválido")
    return redirect('/')

@login_required(login_url='/login/') #qnd ñ tiver autenticado, é levado para tal endereço
def lista_eventos(request):
    usuario = request.user #pegando o user q está fzd a requisição, assim se consegue fazer uma consulta por ele
    data_atual = datetime.now() - timedelta(hours=1) #evento com até uma hora de iniciado, será exibido
    evento = Evento.objects.filter(usuario=usuario,#mesma coisa do all, mas c/ parâmetro na filtragem, só vai retornar os eventos do usuario logado
                                   data_evento__gt=data_atual) #__gt retorna os futuros; __lt retorna os passados
    #evento = Evento.objects.all()
    dados = {'eventos':evento} #evento agora é no plural
    return render(request, 'agenda.html', dados)

@login_required(login_url='/login/')
def evento(request):
    id_evento = request.GET.get('id')
    dados = {}
    if id_evento:
        dados['evento'] = Evento.objects.get(id=id_evento)
        try:
            dados['evento'] = Evento.objects.get(id=id_evento)
        except Exception:
            raise Http404()
    return render(request, 'evento.html', dados)

@login_required(login_url='/login/')
def submit_evento(request):
    if request.POST:
        titulo = request.POST.get('titulo')
        data_evento = request.POST.get('data_evento')
        descricao = request.POST.get('descricao')
        usuario = request.user
        id_evento = request.POST.get('id_evento')
        if id_evento:
            evento = Evento.objects.get(id=id_evento)
            if evento.usuario == usuario:
                evento.titulo = titulo
                evento.descricao = descricao
                evento.data_evento = data_evento
                evento.save()
            # Evento.objects.filter(id=id_evento).update(titulo=titulo,
            #                                           data_evento=data_evento,
            #                                           descricao=descricao)
        else:
            Evento.objects.create(titulo=titulo,
                                  data_evento=data_evento,
                                  descricao=descricao,
                                  usuario=usuario)  #na listagem era um objects.filter, aqui é um objects.create
    return redirect('/')

@login_required(login_url='/login/')
def delete_evento(request, id_evento):
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

def json_lista_evento(request, id_usuario):
    usuario = User.objects.get(id=id_usuario)
    evento = Evento.objects.filter(usuario=usuario).values('id', 'titulo')
    return JsonResponse(list(evento), safe=False) #precisa do safe pq está sendo passado uma Lista e ñ um dicionário


def lista_eventos_historico(request):
    usuario = request.user
    data_atual = datetime.now()
    evento = Evento.objects.filter(usuario=usuario,
                                   data_evento__lt=data_atual)
    dados = {'eventos':evento}
    return render(request, 'historico.html', dados)

def handler404(request, exception):
    return render(request, '404.html')