from email.policy import default
from django.db import models
import datetime
from django.utils import timezone
from django.contrib import admin

""""Represent like django.db.models.Model"""

# models Question 
class Question(models.Model):
    # question 
    question_text = models.CharField(max_length=255)
    # date posted
    pub_date = models.DateTimeField('date publised')
    # Directlty representation of this object
    def __str__(self):
        return self.question_text
    # Improve representation at admin view for 
    # column was_published_recently
    @admin.display(
        boolean=True,
        ordering='pub_date',
        description='Published recently?',
    ) 
    # Custom method
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

# models Choice
class Choice(models.Model):
    # related to single Question
    question = models.ForeignKey(Question, on_delete = models.CASCADE)
    # Choise
    choice_text = models.CharField(max_length = 255)
    # Mount votes
    votes = models.IntegerField(default = 0)
    # Representive direct of this object 
    def __str__(self):
        return self.choice_text
        