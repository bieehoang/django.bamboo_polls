from asyncio import futures
from nntplib import ArticleInfo
from os import times
from re import U
from urllib import response
from django.test import TestCase
import datetime
from django.utils import timezone
from polls.models import Question
from django.urls import reverse
# Create your tests here.

class QuestionModelTests(TestCase):
    def test_check_question_from_future(self):
        """"
        function test_check_question_from_future will return False for question 
        whose pub_date is in the future
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date = time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_check_question_from_older_day(self):
        """
        function return False for questions whose pub_date is older than 1 day
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date = time)
        self.assertIs(old_question.was_published_recently(), False)
    
    def test_check_question_from_recently(self):
        """
        function return True for question whose pub_date is within the last day
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True) 


def create_question(question_text, days):
    """
    Create a question with the given 'question_text' and published the given number of 'days'
    offset to now (NEGATIVE for questions published in the past, POSITIVE for
    questions that have yet to ve published).
    """
    time = timezone.now() + datetime.timedelta(days = days)
    return Question.objects.create(question_text=question_text, pub_date = time)

class QuestionIndexViewTests(TestCase):
    
    def test_no_question(self):
        """
        If no question exists, an appropriate message is displayed
        """
        response =  self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls available")
        self.assertQuerysetEqual(response.context['lastest_question_list'],[])
    
    def test_past_question(self):
        """
        Questions with a pub_date in the past are displayed on the index page
        """
        question = create_question(question_text="PAST QUESTION", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['lastest_question_list'],[question],)
    
    def test_future_question(self):
        """
        Questions with a pub_date in the future are NOT displayed on the index page
        """
        create_question(question_text='FUTURE QUESTION', days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls available")
        self.assertQuerysetEqual(response.context['lastest_question_list'], [])
    
    def test_future_question_and_past_question(self):
        """
        even if both past and future questions exits, only past questions are displayed
        """
        question = create_question(question_text="PAST QUESTION", days = -30)
        create_question(question_text='FUTURE QUESTION', days=30)
        response = self.client.get(reverse('polls:index'))        
        self.assertQuerysetEqual(response.context['lastest_question_list'], [question],)
    
    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions
        """
        question1 = create_question(question_text='PAST QUESTION 1', days = -30)
        question2 = create_question(question_text="PAST QUESTION 2", days = -5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['lastest_question_list'], [question2, question1])

class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future return a 404 not found
        """
        future_question = create_question(question_text="FUTURE QUESTION", days = 5)
        url = reverse('polls:detail', args=(future_question.id, ))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
    
    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past displays the question's text.
        """
        past_question = create_question(question_text="PAST QUESTION", days = -5)
        url = reverse('polls:detail', args=(past_question.id, ))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)