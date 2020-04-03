from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import (get_object_or_404, render)
from django.urls import reverse
from django.utils import timezone
from django.views import generic

from .models import Choice, Question

# def index(request):
#     # return HttpResponse("index")

#     # latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     # output = ', '.join([q.question_text for q in latest_question_list])
#     # return HttpResponse(output)

#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     context = {'latest_question_list': latest_question_list}
#     return render(request, 'polls/index.html', context)


class IndexView(generic.ListView):
    """for ListView, automatically generated context variable is question_list."""
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """ Return the last five published questions.
        (not including those set to be published in the future)."""
        # return Question.objects.order_by('-pub_date')[:5]
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]

# def detail(request, question_id):
#     # return HttpResponse("detail %s" % question_id)

#     # try:
#     #     question = Question.objects.get(pk=question_id)
#     # except Question.DoesNotExist:
#     #     raise Http404('Questin does not exit')
#     # return render(request, 'polls/detail.html', {'question': question})

#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/detail.html', {'question': question, })
class DetailView(generic.DetailView):
    """for DetailView, automatically generated context variable is question."""
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())

# def results(request, question_id):
#     # response = "results %s"
#     # return HttpResponse(response % question_id)

#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/results.html', {'question': question})
class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):  # form => only logic,no template, HttpResponseRedirect
    # return HttpResponse("vote %s" % question_id)
    question = get_object_or_404(Question, pk=question_id)
    print(request.POST)

    try:
        selected_choice = question.choice_set.get(pk=request.POST['choices'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {'question': question, 'error_message': 'You didn\'t select a choice.', })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
