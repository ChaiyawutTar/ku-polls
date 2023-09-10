import datetime
from django.db import models
from django.utils import timezone
from django.contrib import admin

# Create your models here.
class Question(models.Model):
    """
    Represents a poll question.

    Attributes:
        question_text (str): The text of the question.
        pub_date (datetime): The publication date of the question.
        end_date (datetime): The ending date for voting on the question.
    """
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('data published', default=timezone.now)
    end_date = models.DateTimeField('data end', null=True)

    # def was_published_recently(self):
    #     now = timezone.now()
    #     return now - datetime.timedelta(day=1) <= self.pub_date <= now
    @admin.display(
        boolean=True,
        ordering="pub_date",
        description="Published recently?",
    )
    def was_published_recently(self):
        """
        Returns True if the question was published within the last day.
        """
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    
    def is_published(self):
        """
        Returns True if the current local date is on or after the question's publication date.
        """
        now = timezone.localtime(timezone.now())
        return now >= self.pub_date
    
    def can_vote(self):
        """
        Returns True if voting is allowed for this question.
        That means, the current local date/time is between the pub_date and end_date.
        If end_date is null, then voting is allowed anytime after pub_date.
        """
        now = timezone.localtime(timezone.now())
        if self.end_date is None:
            return self.pub_date <= now
        else:
            return self.pub_date <= now <= self.end_date
        # return self.pub_date <= now and (self.end_date is None or now <= self.end_date)


    def __str__(self) -> str:
        return self.question_text

class Choice(models.Model):
    """
    Represents a choice for a poll question.

    Attributes:
        question (Question): The question to which this choice belongs.
        choice_text (str): The text of the choice.
        votes (int): The number of votes received for this choice.
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.choice_text
