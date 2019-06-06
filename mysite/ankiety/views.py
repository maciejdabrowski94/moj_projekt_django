from django.shortcuts import render
from django.http import Http404
from django.http import HttpResponse
from django.template import loader

from .models import Question

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {
        'latest_question_list': latest_question_list,
    }
    return render(request, 'ankiety/index.html', context)

def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Pytanie nie istnieje")
    return render(request, 'ankiety/detail.html', {'question': question})

def results(request, question_id):
    response = "Przegladasz wyniki pytania: %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("Glosujesz w pytaniu: %s." % question_id)
