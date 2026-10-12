from datetime import date

from django import forms

from .models import Registration


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Registration
        fields = ["parent_name", "baby_name", "phone", "baby_birth_date"]
        widgets = {
            "parent_name": forms.TextInput(attrs={"id": "name", "placeholder": "Сергей Иванов"}),
            "baby_name": forms.TextInput(attrs={"id": "baby-name", "placeholder": "Иван Иванович"}),
            "phone": forms.TextInput(attrs={"id": "phone", "type": "tel", "placeholder": "+7 900 000 0000"}),
            "baby_birth_date": forms.DateInput(attrs={"id": "dob", "type": "date"}, format="%Y-%m-%d"),
        }

    def clean_baby_birth_date(self):
        d = self.cleaned_data["baby_birth_date"]
        if d > date.today():
            raise forms.ValidationError(
                "Дата рождения не может быть в будущем.")
        return d
