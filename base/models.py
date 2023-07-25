from django.db import models
from django.contrib.auth.models import User
# from django.conf import settings
# User = settings.AUTH_USER_MODEL

class Quiz(models.Model):
    name = models.CharField(max_length=120)
    topic = models.CharField(max_length=120)
    number_of_questions = models.IntegerField()
    time = models.IntegerField(help_text="Duration of quiz in minutes")

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.topic}"

    def get_questions(self):
        return self.question_set.all()

class Question(models.Model):
    text = models.CharField(max_length=500)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text
    
    def get_answers(self):
        return self.answer_set.all()

class Answer(models.Model):
    text = models.CharField(max_length=200)
    correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text
    
class Result(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.FloatField()

    created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.pk)
    