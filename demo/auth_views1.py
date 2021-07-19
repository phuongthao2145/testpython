from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.contrib.auth import logout
from django.http import HttpResponse
from .forms import LoginForm
from .forms import RegisterForm


def register(request):
    if request.method == 'POST':
        response = HttpResponse()
        response.write("<h1>Thanks for registering</h1></br>")
        response.write("Your username: " + request.POST['username'] + "</br>")
        response.write("Your email: " + request.POST['email'] + "</br>")
        return response

    form = RegisterForm()
    return render(request, 'user_auth/register.html', {'form': form})

def LoginView(request):
    # username = request.POST['username']
    # password = request.POST['password']
    # user = authenticate(request, username=username, password=password)
    print('login')
    form = LoginForm()
    return render(request, 'authticate/login.html', {'form': form})


def logout_view(request):
    logout(request)
    # Redirect to a success page.