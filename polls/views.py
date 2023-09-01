from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.template import loader
from django.http import Http404
from django.urls import reverse
from django.views import generic
from .models import Question, Choice

class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "lastest_question_list"

    def get_queryset(self) -> QuerySet[Any]:
        """Return the last five published questions."""
        return Question.objects.order_by("-pub_date")[:5]
    

class DetailView(generic.DetailView):
    model = Question
    template_nam = 'polls/detail.html'

class ResultView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

    
def index(request : HttpRequest) -> HttpResponse:
    lastest_question_list =  Question.objects.order_by("-pub_date")[:5]
    # template = loader.get_template("polls/index.html")
    context = {
        "lastest_question_list" : lastest_question_list
    }
    # output = ", ".join([q.question_text for q in lastest_question_list])
    return render(request, "polls/index.html", context)

# def detail(request : HttpRequest, question_id) -> HttpResponse: 
#     try:
#         question = Question.objects.get(pk=question_id)
#     except:
#         raise Http404("Question does not exist.")
#     return render(request, "polls/detail.html", {"question" : question})

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/detail.html", {"question": question})

def results(request: HttpRequest, question_id) -> HttpResponse:
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/results.html", {"question": question})

def vote(request : HttpRequest, question_id) -> HttpResponse:
    question = get_object_or_404(Question, pk=question_id)
    try:
        select_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/detail.html/",
            {
                "question" : question,
                "error_message" : "You didn't select a choice.",
            },
        )
    else:
        select_choice += 1
        select_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.

    return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
    



