from django.contrib import messages
from django.shortcuts import redirect, render

from .forms import RegistrationForm


def index(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Регистрация прошла успешно!")
            return redirect("index")
    else:
        form = RegistrationForm()
    return render(request, "index.html", {"form": form})


def index(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Регистрация прошла успешно!")
            return redirect("index")
        else:
            print("ОШИБКИ ФОРМЫ:", form.errors.as_json())
            print("ПОЛУЧЕНО:", dict(request.POST))
    else:
        form = RegistrationForm()
    return render(request, "index.html", {"form": form})
