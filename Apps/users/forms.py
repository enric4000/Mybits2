from datetime import date
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from Apps.users.models import CustomUser
import re


class RegisterForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = "__all__"
        exclude = [
            "emailVerified",
            "is_staff",
            "is_active",
            "is_superuser",
            "last_login",
            "user_permissions",
            "name",
            "groups",
            "Groups",
            "date_joined",
        ]
        labels = {
            "email": "Email",
            "password": "Password",
            "username": "Username",
            "first_name": "First Name",
            "last_name": "Last Name",
            "gender": "Gender",
            "gender_other": "Gender (other)",
            "pronoun": "Your pronouns",
            "date_of_birth": "Date of birth",
            "dietary": "Dietary preference",
            "dietary_other": "Dietary preference (other)",
        }
        # You should add the section text, on the first field you want to be in the section
        help_texts = {
            "email": "Login info 📧",
            "password": "",
            "username": "Personal info 👤",
            "first_name": "",
            "last_name": "",
            "gender": "",
            "gender_other": "",
            "pronoun": "",
            "date_of_birth": "",
            "dietary": "Logistics info 📢",
            "dietary_other": "",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if field.label != "Password":
                if field.label != "Date of birth":
                    field.widget.attrs.update({"class": "form-input"})
                else:
                    field.widget = forms.DateInput(
                        attrs={"type": "date", "class": "form-input"}
                    )
            else:
                field.widget = forms.PasswordInput(attrs={"class": "form-input"})

    def clean_date_of_birth(self):
        date_of_birth = self.cleaned_data.get("date_of_birth")
        errors = []
        # Validations
        if date_of_birth > date.today():
            errors.append("Your date of birth must be in the past.")
        if errors:
            raise forms.ValidationError(errors)
        return date_of_birth

    def clean_password(self):
        password = self.cleaned_data.get("password")
        errors = []
        # Validations
        if len(password) < 8:
            errors.append("Password must be at least 8 characters long.")
        if not re.search(r"[a-z]", password):
            errors.append("Password must contain at least one lowercase letter.")
        if not re.search(r"[A-Z]", password):
            errors.append("Password must contain at least one uppercase letter.")
        if not re.search(r"\d", password):
            errors.append("Password must contain at least one digit.")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            errors.append("Password must contain a symbol like !@#$%).")
        if errors:
            raise forms.ValidationError(errors)
        return password


class CustomLoginForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ["email", "password"]
        labels = {
            "Email": "Email",
            "password": "Password",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-input"})
