from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Quiz, Question, Answer, Result
from loginsys.models import Teacher
from django.http import JsonResponse
from .forms import QuestionForm, AnswerForm

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

@login_required(login_url='login')
def resultPage(request):
    user = request.user
    results = Result.objects.filter(user=user)
    result = results.order_by('-created').first()
    print("Final result", result)

    context = {"result": result}
    return render(request, "base/result.html", context)


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

    if request.method == 'POST':
        name = request.POST.get('quiz-name')
        topic = request.POST.get('quiz-topic')
        total_questions = request.POST.get('quiz-total_questions')
        time = request.POST.get('quiz-time')

        Quiz.objects.create(
            name = name,
            topic = topic,
            number_of_questions = total_questions,
            time = time
        )

        return redirect('question')

    context = {}
    return render(request, 'base/create-quiz.html', context)

@login_required(login_url='login')
def question(request):

    try:
        teacher = Teacher.objects.get(user=request.user)
    except:
        return redirect('home')

    form = QuestionForm()

    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('answer')

    context = {'form': form}
    return render(request, 'base/question.html', context)

@login_required(login_url='login')
def answer(request):

    try:
        teacher = Teacher.objects.get(user=request.user)
    except:
        return redirect('home')

    form = AnswerForm()

    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('answer')

    context = {'form': form}
    return render(request, 'base/answers.html', context)

