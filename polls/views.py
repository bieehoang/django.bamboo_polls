from urllib import request
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from .models import Choice, Question


# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     context = {
#         'latest_question_list': latest_question_list,
#     }
#     return render(request, 'polls/index.html', context)


# def details(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)

#     return render(request, 'polls/details.html', {'question': question})


# def results(request, question_id):
#     question = get_object_or_404(Question, pk = question_id)
#     return render(request,'polls/result.html', {'question': question})

## Update:

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'lastest_question_list'
    def get_queryset(self):
        """
        Return the last 5 published question
        ** NOT INCLUDING THOSE SET TO BE PUBLISHED IN THE FUTURE **
        """
        return Question.objects.filter(
            pub_date__lte = timezone.now()
        ).order_by('-pub_date')[:5]
class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/details.html'
    def get_queryset(self):
        """
        excludes any questions that are NOT published yet
        """
        return Question.objects.filter(pub_date__lte = timezone.now())

class ResultView(generic.DetailView):
    model = Question
    template_name = 'polls/result.html'

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk = request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/details.html', {
            'question': question,
            'error message': 'You didn\'t select a choice  '
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args = (question.id, )))
