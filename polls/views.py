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
from .models import Question, Choice , Vote
from django.db.models import Q
from django.contrib.auth.decorators import login_required

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
        now = timezone.now()
        return Question.objects.filter(
            Q(pub_date__lte=now) & (Q(end_date__gte=now) | Q(end_date=None))
        ).order_by("-pub_date")
    

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



@login_required
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
    # if not request.user.is_authenticated():
    #     # user must login to vote
    #     redirect('login')
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
    this_user = request.user
    #selected_choice.votes += 1
    #selected_choice.save()
    try:
        # find a vote for this user and this question
        vote = Vote.objects.get(user=this_user, choice__question=question)
        # update his vote
        vote.choice = selected_choice
    except Vote.DoesNotExist:
        # no matching vote - create a new Vote
        vote = vote.objects.create(user=request.user, choice=selected_choice)
    # if the user has a vote for this question
    #     update his vote for selected_choice
    # else : 
    #     create a new vote for this user and choice
    #     save it 
    vote.save()
    # TODO: USe messages to display a confirmation on the results page.
    return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
    



