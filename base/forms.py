from django import forms
from django.forms import inlineformset_factory
from .models import Answer, Question, Quiz

class QuizForm(forms.ModelForm):

    class Meta:
        model = Quiz
        fields = '__all__'
        exclude = ['teacher']

class QuestionForm(forms.ModelForm):

    class Meta:
        model = Question
        fields = ['text']

class AnswerForm(forms.ModelForm):

    class Meta:
        model = Answer
        fields = ['text', 'correct']

AnswerFormSet = inlineformset_factory(Question, Answer, form=AnswerForm, extra=3)