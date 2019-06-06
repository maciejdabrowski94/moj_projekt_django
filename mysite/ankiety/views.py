from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. Jesets na stronie ANKIETY.")

def detail(request, question_id):
    return HttpResponse("Ogladasz pytanie: %s." % question_id)

def results(request, question_id):
    response = "Przegladasz wyniki pytania: %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("Glosujesz w pytaniu: %s." % question_id)
