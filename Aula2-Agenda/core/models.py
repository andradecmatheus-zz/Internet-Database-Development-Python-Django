from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Evento(models.Model):
    titulo = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True) #pode ficar em branco e ser nulo
    data_evento = models.DateTimeField(verbose_name='Data do Evento') #configura a label
    data_criacao = models.DateTimeField(auto_now=True) #inseri automaticamente
    usuario = models.ForeignKey(User, on_delete=models.CASCADE) #cascade: se o usuário for escluido da app, tudo dele tbm será

    class Meta:
        db_table = 'evento' #exige q o nome da tabela será evento)

    def __str__(self):#sempre q alguem chamar o objeto título, será trazido o nome do título,
        return self.titulo #mesmo q ñ seja clicado p/ acessar algum campo do evento (evento object ñ mais)

    def get_data_evento(self): #é possível criar uma função aqui no models e chamá-la no html
        return self.data_evento.strftime('%d/%m/%Y %H:%M Hrs')

    def get_data_input_evento(self):
        return self.data_evento.strftime('%Y-%m-%dT%H:%M') #padrão de string para reconhecimento do tipo datetime-local em eventos.html