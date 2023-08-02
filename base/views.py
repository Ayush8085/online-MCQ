from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Quiz, Question, Answer, Result
from loginsys.models import Teacher
from django.http import JsonResponse
from .forms import QuestionForm, QuizForm, AnswerFormSet

def homePage(request):
    quizes = Quiz.objects.all()

    context = {"quizes": quizes}
    return render(request, "base/home.html", context)

@login_required(login_url='login')
def quiz(request, pk):
    quiz = Quiz.objects.get(id=pk)

    score = 0
    if request.method == "POST":
        questions = []
        data = request.POST
        data = dict(data.lists())
        data.pop('csrfmiddlewaretoken')
        
        for k in data.keys():
            print("key: ", k)
            question = Question.objects.get(text=k)
            questions.append(question)
        print(questions)

        for q in questions:
            a_selected = request.POST.get(q.text)
            
            question_answers = Answer.objects.filter(question=q)
            for a in question_answers:
                if a_selected == a.text:
                    if a.correct:
                        score += 1

        
        Result.objects.create(quiz=quiz, user=request.user, score=score)
        return redirect('result')

    context = {"quiz": quiz}
    return render(request, "base/quiz.html", context)


def quizData(request, pk):
    quiz = Quiz.objects.get(id=pk)

    questions = []
    for q in quiz.get_questions():
        answers = []
        for a in q.get_answers():
            answers.append(a.text)
        questions.append({str(q): answers})
    
    return JsonResponse({
        "data": questions,
        "time": quiz.time,
    })

@login_required(login_url='login')
def createQuiz(request):

    try:
        teacher = Teacher.objects.get(user=request.user)
    except:
        return redirect('home')

    quiz_form = QuizForm()

    if request.method == 'POST':
        quiz_form = QuizForm(request.POST)

        if quiz_form.is_valid():
            form = quiz_form.save(commit=False)
            form.teacher = teacher
            form.save()
            return redirect('questions')

    context = {'quiz_form': quiz_form}
    return render(request, 'base/create-quiz.html', context)

@login_required(login_url='login')
def createQuestions(request):

    try:
        teacher = Teacher.objects.get(user=request.user)
    except:
        return redirect('home')
    
    question_form = QuestionForm()
    answer_formset = AnswerFormSet(instance=Question())
    
    quiz = teacher.quiz_set.all().order_by('-created').first()

    number_of_questions = quiz.number_of_questions

    if request.method == 'POST':

        question_form = QuestionForm(request.POST)
        answer_formset = AnswerFormSet(request.POST, instance=Question())
        
        if question_form.is_valid() and answer_formset.is_valid():
          question = question_form.save(commit=False)
          question.quiz = quiz
          question.save()

          answer_formset.instance = question
          answer_formset.save()
          
          return redirect('home')

    context = {'question_form': question_form, 'answer_formset': answer_formset, 'number_of_questions': range(1, number_of_questions+1)}
    return render(request, 'base/questions.html', context)


@login_required(login_url='login')
def resultPage(request):
    user = request.user
    results = Result.objects.filter(user=user)
    result = results.order_by('-created').first()
    print("Final result", result)

    context = {"result": result}
    return render(request, "base/result.html", context)

