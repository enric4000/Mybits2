from django.forms import ValidationError
from django.db.models import Q

from Apps.participant.services import ParticipantService
from .models import CustomUser


class UserService:
    @staticmethod
    def create_user(form):
        """
        Create a new user using the provided form data.
        """
        user = form.save(commit=True)
        user.set_password(form.cleaned_data["password"])
        user.save()
        return user

    @staticmethod
    def update_user(form, user):
        """
        Update an existing user using the provided form data.
        """
        user = form.save(commit=True)
        user.set_password(form.cleaned_data["password"])
        user.save()
        return user

    @staticmethod
    def delete_user(user):
        """
        Delete an existing user using the provided form data.
        """
        ParticipantService.delete_user_from_participant(user)

        user.delete()
        return True

    @staticmethod
    def get_user(id):
        """
        Retrieve an existing user using the provided form data.
        """
        try:
            user = CustomUser.objects.get(id=id)
        except (ValidationError, CustomUser.DoesNotExist) as exc:
            raise exc
        return user

    @staticmethod
    def get_first_100_users():
        """
        Retrieve the first 100 users from the database.
        """
        users = CustomUser.objects.all()[:100]
        return users

    @staticmethod
    def find_by_name_and_email(search):
        """
        Retrieve users by name or email.
        """
        users = CustomUser.objects.filter(
            Q(username__icontains=search)
            | Q(email__icontains=search)
            | Q(first_name__icontains=search)
            | Q(last_name__icontains=search)
        )
        return users
