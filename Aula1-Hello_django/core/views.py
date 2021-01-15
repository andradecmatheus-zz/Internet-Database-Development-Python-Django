from django.shortcuts import render, HttpResponse


# Create your views here.

def hello(request, nome, idade):
    return HttpResponse('<h1>Hello {} de {} anos</h1>'.format(nome, idade))

def soma(request, a, b):
    return HttpResponse('<h1>A soma de {} + {} é {}</h1>'.format(a, b, a+b))

def sub(request, a, b):
    return HttpResponse('<h1>A subtração de {} - {} é {}</h1>'.format(a, b, a-b))

def mult(request, a, b):
    return HttpResponse('<h1>A multiplicação de {} * {} é {}</h1>'.format(a, b, a*b))

def div(request, a, b):
    return HttpResponse('<h1>A divisão de {} / {} é {}</h1>'.format(a, b, a/b))
