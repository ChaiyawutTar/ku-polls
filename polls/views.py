from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.template import loader
from django.http import Http404
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages
from .models import Question, Choice

class IndexView(generic.ListView):
    """
    View for displaying the list of the latest published questions.

    Attributes:
        template_name (str): The name of the template to render.
        context_object_name (str): The name of the context variable containing the question list.
    """


    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self) -> QuerySet[Any]:
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[
            :5
        ]
    # def get_queryset(self):
    #     """
    #     Excludes any questions that aren't published yet.
    #     """
    #     return Question.objects.filter(pub_date__lte=timezone.now())
    

class DetailView(generic.DetailView):
    """
    View for displaying the details of a specific question.

    Attributes:
        model: The model class to use for this view.
        template_name (str): The name of the template to render.
    """
    model = Question
    template_name = 'polls/detail.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        # Check if the poll is votable
        if not self.object.can_vote():
            raise Http404("This poll is closed and cannot be voted on.")

        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)
    
    def get_queryset(self) -> QuerySet[Any]:
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


# def index(request : HttpRequest) -> HttpResponse:
#     lastest_question_list =  Question.objects.order_by("-pub_date")[:5]
#     # template = loader.get_template("polls/index.html")
#     context = {
#         "lastest_question_list" : lastest_question_list
#     }
#     # output = ", ".join([q.question_text for q in lastest_question_list])
#     return render(request, "polls/index.html", context)

# def detail(request : HttpRequest, question_id) -> HttpResponse: 
#     try:
#         question = Question.objects.get(pk=question_id)
#     except:
#         raise Http404("Question does not exist.")
#     return render(request, "polls/detail.html", {"question" : question})

# def detail(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, "polls/detail.html", {"question": question})

# def results(request: HttpRequest, question_id) -> HttpResponse:
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, "polls/results.html", {"question": question})

def vote(request, question_id):
    """
    Handle the voting process for a specific poll question.

    Args:
        request (HttpRequest): The HTTP request object.
        question_id (int): The ID of the question being voted on.

    Returns:
        HttpResponse: A redirect to the results page if the vote is successful, or a re-rendered voting form if there is an error.
    """
    question = get_object_or_404(Question, pk=question_id)
    if not question.can_vote():
        messages.error(request, "Voting is not allowed for this question.")
        return redirect("polls:index")
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
    



