from datetime import date

from django import forms
from django.contrib.auth.password_validation import validate_password

from .models import User, normalize_phone


class RegistrationForm(forms.Form):
    parent_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(
            attrs={"id": "name", "placeholder": "Сергей Иванов"}),
    )
    baby_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(
            attrs={"id": "baby-name", "placeholder": "Иван Иванович"}),
    )
    phone = forms.CharField(
        max_length=20,
        widget=forms.TextInput(
            attrs={"id": "phone", "type": "tel", "placeholder": "+7 900 000 0000"}),
    )
    baby_birth_date = forms.DateField(
        widget=forms.DateInput(
            attrs={"id": "dob", "type": "date"}, format="%Y-%m-%d"),
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"id": "password1"}))
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"id": "password2"}))

    def clean_phone(self):
        phone = normalize_phone(self.cleaned_data["phone"])
        if not 11 <= len(phone) <= 16:
            raise forms.ValidationError("Введите корректный номер телефона.")
        if User.objects.filter(phone=phone).exists():
            raise forms.ValidationError("Этот телефон уже зарегистрирован.")
        return phone

    def clean_baby_birth_date(self):
        d = self.cleaned_data["baby_birth_date"]
        if d > date.today():
            raise forms.ValidationError(
                "Дата рождения не может быть в будущем.")
        return d

    def clean(self):
        cleaned = super().clean()
        p1, p2 = cleaned.get("password1"), cleaned.get("password2")
        if p1 and p2:
            if p1 != p2:
                self.add_error("password2", "Пароли не совпадают.")
            else:
                try:
                    validate_password(p1)
                except forms.ValidationError as e:
                    self.add_error("password1", e)
        return cleaned

    def save(self):
        d = self.cleaned_data
        return User.objects.create_user(
            phone=d["phone"],
            password=d["password1"],
            parent_name=d["parent_name"],
            baby_name=d["baby_name"],
            baby_birth_date=d["baby_birth_date"],
        )


class LoginForm(forms.Form):
    phone = forms.CharField(
        widget=forms.TextInput(
            attrs={"type": "tel", "placeholder": "+7 900 000 0000"})
    )
    password = forms.CharField(widget=forms.PasswordInput)
