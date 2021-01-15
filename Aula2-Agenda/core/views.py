from django.shortcuts import render, redirect
from core.models import Evento
# Create your views here.

#def index (request):
#    return redirect('/agenda/')

def lista_eventos(request):
    #usuario = request.user #pegando o user q está fzd a requisição, assim se consegue fazer uma consulta por ele
    #evento = Evento.objects.filter(usuario=usuario) #mesma coisa do all, mas com parâmetro na filtragem, só vai retornar os eventos do usuario logado
    evento = Evento.objects.all()
    dados = {'eventos':evento} #evento agora é no plural
    return render(request, 'agenda.html', dados)