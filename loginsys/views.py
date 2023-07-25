from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import SignupForm
from django.http import HttpResponse
from .models import Teacher, Student


def loginUser(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return HttpResponse("Something went wrong")

    return render(request, 'loginsys/login.html')

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerUser(request):
    form = SignupForm()

    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            role = request.POST['role']
            print(role)
            login(request, user)
            if(role == 'teacher'):
                Teacher.objects.create(
                    user=request.user,
                    name=request.POST['username'],
                    email = request.POST['email']
                )
            else:
                Student.objects.create(
                    user=request.user,
                    name=request.POST['username'],
                    email = request.POST['email']
                )
            return redirect('home')

    context = {'form': form}
    return render(request, 'loginsys/registerUser.html', context)
