from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpRequest
from django.template import loader
from django.http import Http404
from .models import Question

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
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request : HttpRequest, question_id) -> HttpResponse:
    return HttpResponse("You're voting on question %s." % question_id)





