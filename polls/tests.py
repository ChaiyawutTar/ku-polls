import datetime

from django.test import TestCase, Client
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Question, Choice, Vote
from .views import SignUpView

class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)
        
    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for questions whose pub_date
        is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

    def test_is_published_future_pub_date(self):
        """
        is_published() should return False for a question with a future pub date.
        """
        future_pub_date = timezone.now() + timezone.timedelta(days=1)
        question = Question(pub_date=future_pub_date)
        self.assertFalse(question.is_published())
    
    def test_is_published_default_pub_date(self):
        """
        is_published() should return True for a question with the default pub date (now).
        """
        current_time = timezone.now()
        question = Question(pub_date=current_time)
        self.assertTrue(question.is_published())

    def test_is_published_past_pub_date(self):
        """
        is_published() should return True for a question with a pub date in the past.
        """
        past_pub_date = timezone.now() - timezone.timedelta(days=1)
        question = Question(pub_date=past_pub_date)
        self.assertTrue(question.is_published())

    def test_can_vote_when_end_date_is_none(self):
        """
        can_vote() should return True when end_date is None, indicating that voting is allowed anytime after pub_date.
        """
        question = Question()
        self.assertTrue(question.can_vote())

    def test_can_vote_within_voting_period(self):
        """
        can_vote() should return True when the current time is within the voting period (between pub_date and end_date).
        """
        current_time = timezone.now()
        future_end_date = current_time + timezone.timedelta(days=1)
        question = Question(pub_date=current_time, end_date=future_end_date)
        self.assertTrue(question.can_vote())

    def test_cannot_vote_after_end_date(self):
        """
        can_vote() should return False if the end_date is in the past, indicating that voting is not allowed.
        """
        past_end_date = timezone.now() - timezone.timedelta(days=1)
        question = Question(end_date=past_end_date)
        self.assertFalse(question.can_vote())

    def test_cannot_vote_before_pub_date(self):
        """
        can_vote() should return False if the current time is before the pub_date, indicating that voting is not allowed.
        """
        future_pub_date = timezone.now() + timezone.timedelta(days=1)
        question = Question(pub_date=future_pub_date)
        self.assertFalse(question.can_vote())
    
        

# dadad
def create_question(question_text, days):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["latest_question_list"], [])

    def test_past_question(self):
        """
        Questions with a pub_date in the past are displayed on the
        index page.
        """
        question = create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question],
        )

    def test_future_question(self):
        """
        Questions with a pub_date in the future aren't displayed on
        the index page.
        """
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["latest_question_list"], [])



    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        are displayed.
        """
        question = create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question],
        )

    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        question1 = create_question(question_text="Past question 1.", days=-30)
        question2 = create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question2, question1],
        )

class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future
        returns a 404 not found.
        """
        future_question = create_question(question_text="Future question.", days=5)
        url = reverse("polls:detail", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past
        displays the question's text.
        """
        past_question = create_question(question_text="Past Question.", days=-5)
        url = reverse("polls:detail", args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)
    
class SignUpViewTests(TestCase):
    def test_signup_view_exists(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)

    def test_signup(self):
        response = self.client.post(reverse('signup'), {
            'username': 'newuser',
            'password1': 'newpassword',
            'password2': 'newpassword',
        })
        self.assertEqual(response.status_code, 200)  # Check if signup is successful

    def test_redirect(self):
        signup_url = reverse("signup")
        data = {
            'username': 'tester_signup',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }
        response = self.client.post(signup_url, data)
        self.assertRedirects(response, reverse("polls:index"))



class VoteTests(TestCase):
    def setUp(self):
        # Create a test user
        self.test_user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )

        # Create a test question
        self.test_question = Question.objects.create(
            question_text='Test Question',
            pub_date=timezone.now(),
            end_date=timezone.now() + timezone.timedelta(days=1)
        )
        self.test_choice = Choice.objects.create(
            question=self.test_question,
            choice_text='Test Choice'
        )
       

    def test_vote(self):
        # Login with the test user
        self.client.login(username='testuser', password='testpassword')

        # Test user's vote on a question
        response = self.client.post(reverse('polls:vote', args=(self.test_question.id,)), {
            'choice': self.test_choice.id,
        })
        self.assertEqual(response.status_code, 302)  # Check if vote is successful

        # Check if the vote is recorded in the database
        self.assertTrue(Choice.objects.filter(pk=self.test_choice.id).exists())

    def test_vote_unauthenticated_user(self):
        # Test voting by an unauthenticated user
        response = self.client.post(reverse('polls:vote', args=(self.test_question.id,)), {
            'choice': self.test_choice.id,
        })
        self.assertEqual(response.status_code, 302)  # Check if the user is redirected to login page

    def test_vote_closed_question(self):
        # Change the end_date of the test question to the past
        self.test_question.end_date = timezone.now() - timezone.timedelta(days=1)
        self.test_question.save()

        # Login with the test user
        self.client.login(username='testuser', password='testpassword')

        # Test user's vote on a closed question
        response = self.client.post(reverse('polls:vote', args=(self.test_question.id,)), {
            'choice': self.test_choice.id,
        })
        self.assertEqual(response.status_code, 302)  # Check if the user receives a 404 error

    def test_vote_invalid_choice(self):
        # Login with the test user
        self.client.login(username='testuser', password='testpassword')

        # Test user's vote with an invalid choice
        response = self.client.post(reverse('polls:vote', args=(self.test_question.id,)), {
            'choice' : 999
        })

        self.assertRedirects(response, reverse('polls:detail', args=(self.test_question.id,)))