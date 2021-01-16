from django.shortcuts import render, redirect
from core.models import Evento
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
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
    evento = Evento.objects.filter(usuario=usuario) #mesma coisa do all, mas com parâmetro na filtragem, só vai retornar os eventos do usuario logado
    #evento = Evento.objects.all()
    dados = {'eventos':evento} #evento agora é no plural
    return render(request, 'agenda.html', dados)