from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import LoginForm, RegistrationForm
from .models import normalize_phone


def index(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)          # сразу входим после регистрации
            return redirect("profile")
    else:
        form = RegistrationForm()
    return render(request, "index.html", {"form": form, "nav": "home"})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=normalize_phone(form.cleaned_data["phone"]),
                password=form.cleaned_data["password"],
            )
            if user is not None:
                login(request, user)
                return redirect("profile")
            form.add_error(None, "Неверный телефон или пароль.")
    else:
        form = LoginForm()
    return render(request, "login.html", {"form": form})


def logout_view(request):
    if request.method == "POST":
        logout(request)
    return redirect("index")


@login_required
def profile(request):
    return render(request, "profile.html", {"nav": "profile"})


def shopping(request):
    return render(request, "shopping.html", {"nav": "shopping"})
