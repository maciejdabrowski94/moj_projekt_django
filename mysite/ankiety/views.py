from django.shortcuts import get_object_or_404, render
from django.http import Http404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Question, Choice

class IndexView(generic.ListView):
    template_name = 'ankiety/index.html'
    context_object_name = 'latest_question_list'
    def get_queryset(self):
        """Zwroc piec ostatnich opublikowanych ankiet(nie uwzgledniajac tych,
         ktore maja byc opublikowane w przyszlosci)."""
        return Question.objects.filter(
            pub_date__lte=timezone.now()
            ).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'ankiety/detail.html'

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'ankiety/results.html'

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        #wyswietl ponownie formularz do glosowania
        return render(request, 'ankiety/detail.html', {
            'question': question,
            'error_message': "Nie dokonales wyboru",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('ankiety:results', args=(question.id,)))
