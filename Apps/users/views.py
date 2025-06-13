from django.forms import ValidationError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.forms.models import model_to_dict
from django.views import View
from django.contrib.auth.views import LoginView
from .models import CustomUser
from .services import UserService
from .forms import RegisterForm, CustomLoginForm


class UsersView(View):
    """
    This view handles the render of the list of users with or without filters.
    """

    template_name = "home.html"

    def get(self, request, *args, **kwargs):
        search = request.GET.get("search")
        if search:
            users = UserService.find_by_name_and_email(search)
        else:
            users = UserService.get_first_100_users()
        return render(request, "users.html", {"users": users}, status=200)


class ProfileView(View):
    """
    This view handles the render of the profile of the user logged in.
    It also handles the update of the user data and the delete of the user,
    and it handles the deletion of the user.
    """

    template_name = "profile.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            user = request.user
        else:
            return redirect("/user/login?next=/user/profile")

        form = RegisterForm(instance=user)
        return render(request, self.template_name, {"form": form}, status=200)

    def post(self, request, *args, **kwargs):
        form = RegisterForm(request.POST, instance=request.user)
        if not request.user.is_authenticated:
            return redirect("/user/login?next=/user/profile", status=401)
        if form.is_valid():
            user = UserService.update_user(form, request.user)
            login(request, user)
            return render(request, self.template_name, {"form": form}, status=200)
        else:
            return render(request, self.template_name, {"form": form}, status=400)

    def delete(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            user = request.user
            logout(request)
            UserService.delete_user(user)
            return HttpResponse(status=204)
        else:
            return redirect("/user/login?next=/user/profile")


class UserProfileView(View):
    """
    This view handles the render of the profile of a random user identified by the id
    """

    template_name = "userProfile.html"

    def get(self, request, *args, **kwargs):
        try:
            user = UserService.get_user(kwargs["pk"])
        except (CustomUser.DoesNotExist, ValidationError):
            return redirect("/")

        excluded_fields = {
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
            "password",
        }
        user_dict = model_to_dict(user)
        user_fields = [
            {"name": key, "value": value}
            for key, value in user_dict.items()
            if key not in excluded_fields
        ]
        return render(request, self.template_name, {"fields": user_fields}, status=200)


class CustomLoginView(LoginView):
    """
    This view handles the render of the login form and the login of the user.
    """

    template_name = "logIn.html"

    def get(self, request, *args, **kwargs):
        form = CustomLoginForm()
        return render(request, self.template_name, {"form": form}, status=200)

    def post(self, request, *args, **kwargs):
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            next_url = request.GET.get("next")

            if next_url:
                return redirect(next_url)

            return redirect("/")

        return render(request, self.template_name, {"form": form}, status=400)


class CustomLogoutView(LoginView):
    """
    This view handles the render of the logout of the user.
    """

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect("/")


class CustomRegisterView(View):
    """
    This view handles the render of the register form and the registration of the user.
    """

    template_name = "register.html"

    def get(self, request, *args, **kwargs):
        form = RegisterForm()
        return render(request, self.template_name, {"form": form}, status=200)

    def post(self, request, *args, **kwargs):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = UserService.create_user(form)
            login(request, user)
            return redirect("/")
        else:
            return render(request, self.template_name, {"form": form}, status=200)
