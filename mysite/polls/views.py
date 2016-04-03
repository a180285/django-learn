from django.shortcuts import render
from django.http import Http404
from django.shortcuts import get_object_or_404, render

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.core.urlresolvers import reverse
from .models import Choice, Question, Loan, Platform
from django.views import generic
from django.utils import timezone

from .tables import LoanTable

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

from django.shortcuts import render
from django_tables2   import RequestConfig

def table(request, min_duration = 0, max_duration = 100):
    min_duration = int(min_duration) * 30
    max_duration = int(max_duration) * 30

    loans = Loan.objects.all().filter(duration__gte= min_duration, 
        duration__lte = max_duration)

    table = LoanTable(loans)
    RequestConfig(request).configure(table)

    platforms = Platform.objects.all().order_by('-last_update_time')

    content = {'table': table,
        'platforms': platforms}

    return render(request, 'polls/table.html', content)
