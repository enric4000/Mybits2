from django import forms
from .models import Participant, Hacker, Mentor, Sponsor, Volunteer, Admin


class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = "__all__"
        exclude = [
            "event",
            "user",
            "accepted_date",
            "application_date",
            "status",
            "type",
        ]
        labels = {
            "phone_number": "Which phone number are you using? (please include the country code)",
            "accepted_terms_and_conditions": "Our terms and conditions",
            "t_shirt_size": "Leave us yout t-shirt size 👕",
            "origin": "Where are you joining us from?",
        }
        # You should add the section text, on the first field you want to be in the section
        help_texts = {
            "phone_number": "General info 📖",
            "accepted_terms_and_conditions": "",
            "t_shirt_size": "",
            "origin": "",
        }
        widgets = {
            "phone_number": forms.TextInput(attrs={"class": "form-input"}),
            "accepted_terms_and_conditions": forms.CheckboxInput(
                attrs={"class": "form-checkbox"}
            ),
            "t_shirt_size": forms.Select(attrs={"class": "form-select"}),
            "origin": forms.TextInput(attrs={"class": "form-input"}),
        }


class HackerForm(ParticipantForm):
    """
    This form is used to create a hacker.
    """

    class Meta(ParticipantForm.Meta):
        model = Hacker
        fields = "__all__"
        exclude = ParticipantForm.Meta.exclude
        labels = {
            **ParticipantForm.Meta.labels,
            "university": "In which university are you studying, or did you study?",
            "degree": "Which degree",
            "graduation_year": "In which year have or you will be graduating?",
            "under_age": "Will you be under age during the event?",
            "lenny_face": "Show us your favourite lenny face ( ͡° ͜ʖ ͡°)!",
            "hear_about_us": "How did you hear about us?",
            "why_excited": "Why are you excited to join us?",
            "first_hackathon": "Is this your first hackathon?",
            "personal_projects": "Tell us about your personal projects",
            "github": "Leave us your GitHub link",
            "devpost": "Leave us your Devpost link",
            "linkedin": "Leave us your LinkedIn link",
            "personal": "Leave us your personal website or project",
            "cv": "Upload your CV",
            "share_cv": "Do you want to share your CV with our sponsors?",
            "subscribe": "Do you want to subscribe to our newsletter?",
        }
        help_texts = {
            **ParticipantForm.Meta.help_texts,
            "university": "Studies info 🎓",
            "degree": "",
            "graduation_year": "",
            "under_age": "",
            "lenny_face": "Let us know more about you 👀",
            "hear_about_us": "",
            "why_excited": "",
            "first_hackathon": "",
            "personal_projects": "",
            "github": "Levave us your links to know more about you 💻!",
            "devpost": "",
            "linkedin": "",
            "personal": "",
            "cv": "",
            "share_cv": "Just two more questions! 📄",
            "subscribe": "",
        }

        widgets = {
            **ParticipantForm.Meta.widgets,
            "university": forms.TextInput(attrs={"class": "form-input"}),
            "degree": forms.TextInput(attrs={"class": "form-input"}),
            "graduation_year": forms.TextInput(attrs={"class": "form-input"}),
            "under_age": forms.CheckboxInput(attrs={"class": "form-checkbox"}),
            "lenny_face": forms.TextInput(attrs={"class": "form-input"}),
            "hear_about_us": forms.TextInput(attrs={"class": "form-input"}),
            "why_excited": forms.Textarea(attrs={"class": "form-input"}),
            "first_hackathon": forms.CheckboxInput(attrs={"class": "form-checkbox"}),
            "personal_projects": forms.Textarea(attrs={"class": "form-input"}),
            "github": forms.TextInput(attrs={"class": "form-input"}),
            "devpost": forms.TextInput(attrs={"class": "form-input"}),
            "linkedin": forms.TextInput(attrs={"class": "form-input"}),
            "personal": forms.TextInput(attrs={"class": "form-input"}),
            "cv": forms.ClearableFileInput(attrs={"class": "form-input"}),
            "share_cv": forms.CheckboxInput(attrs={"class": "form-checkbox"}),
            "subscribe": forms.CheckboxInput(attrs={"class": "form-checkbox"}),
        }


class MentorForm(ParticipantForm):
    """
    This form is used to create a mentor.
    """

    model = Mentor
    fields = "__all__"
    exclude = ParticipantForm.Meta.exclude
    labels = {
        **ParticipantForm.Meta.labels,
        "university": "In which university are you studying, or did you study?",
        "degree": "Which degree?",
        "position": "If you aren't a student, what is your current position?",
        "english_level": "How would you rate your English level?",
        "hear_about_us": "How did you hear about us?",
        "personal_projects": "Tell us about your personal projects",
        "github": "Leave us your GitHub link",
        "devpost": "Leave us your Devpost link",
        "linkedin": "Leave us your LinkedIn link",
        "personal": "Leave us your personal website or project",
        "cv": "Upload your CV",
        "subscribe": "Do you want to subscribe to our newsletter?",
    }
    help_texts = {
        **ParticipantForm.Meta.help_texts,
        "university": "Studies or job position info 🎓",
        "degree": "",
        "position": "",
        "english_level": "Let us know more about you 👀",
        "hear_about_us": "",
        "personal_projects": "",
        "github": "Levave us your links to know more about you 💻!",
        "devpost": "",
        "linkedin": "",
        "personal": "",
        "cv": "Just two more questions! 📄",
        "subscribe": "",
    }
    widgets = {
        **ParticipantForm.Meta.widgets,
        "university": forms.TextInput(attrs={"class": "form-input"}),
        "degree": forms.TextInput(attrs={"class": "form-input"}),
        "position": forms.TextInput(attrs={"class": "form-input"}),
        "english_level": forms.Select(attrs={"class": "form-select"}),
        "hear_about_us": forms.TextInput(attrs={"class": "form-input"}),
        "personal_projects": forms.Textarea(attrs={"class": "form-input"}),
        "github": forms.TextInput(attrs={"class": "form-input"}),
        "devpost": forms.TextInput(attrs={"class": "form-input"}),
        "linkedin": forms.TextInput(attrs={"class": "form-input"}),
        "personal": forms.TextInput(attrs={"class": "form-input"}),
        "cv": forms.ClearableFileInput(attrs={"class": "form-input"}),
        "subscribe": forms.CheckboxInput(attrs={"class": "form-checkbox"}),
    }


class SponsorForm(ParticipantForm):
    """
    This form is used to create a sponsor.
    """

    model = Sponsor
    fields = "__all__"
    exclude = ParticipantForm.Meta.exclude
    labels = {
        **ParticipantForm.Meta.labels,
        "company_name": "What is your company name?",
        "position": "What is your position?",
    }
    help_texts = {
        **ParticipantForm.Meta.help_texts,
        "company_name": "Company info 🏢",
        "position": "",
    }
    widgets = {
        **ParticipantForm.Meta.widgets,
        "company_name": forms.TextInput(attrs={"class": "form-input"}),
        "position": forms.TextInput(attrs={"class": "form-input"}),
    }


class VolunteerForm(ParticipantForm):
    """
    This form is used to create a volunteer.
    """

    model = Volunteer
    fields = "__all__"
    exclude = ParticipantForm.Meta.exclude
    labels = {
        **ParticipantForm.Meta.labels,
        "university": "In which university are you studying, or did you study?",
        "degree": "Which degree?",
        "position": "If you aren't a student, what is your current position?",
        "languages": "Which languages do you speak?",
        "first_volunteering": "Is this your first volunteering?",
        "hear_about_us": "How did you hear about us?",
        "cool_skill": "What is your coolest skill?",
        "personal_qualities": "What are your personal qualities?",
        "personal_weakness": "What are your personal weaknesses?",
        "motivation": "Why do you want to volunteer?",
        "nigth_shifts": "Are you available for night shifts?",
        "subscribe": "Do you want to subscribe to our newsletter?",
    }
    help_texts = {
        **ParticipantForm.Meta.help_texts,
        "university": "Studies or job position info 🎓",
        "degree": "",
        "position": "",
        "languages": "Tell us more about you 👀",
        "first_volunteering": "",
        "hear_about_us": "",
        "cool_skill": "",
        "personal_qualities": "",
        "personal_weakness": "",
        "motivation": "",
        "nigth_shifts": "",
        "subscribe": "",
    }
    widgets = {
        **ParticipantForm.Meta.widgets,
        "university": forms.TextInput(attrs={"class": "form-input"}),
        "degree": forms.TextInput(attrs={"class": "form-input"}),
        "position": forms.TextInput(attrs={"class": "form-input"}),
        "languages": forms.TextInput(attrs={"class": "form-input"}),
        "first_volunteering": forms.CheckboxInput(attrs={"class": "form-checkbox"}),
        "hear_about_us": forms.TextInput(attrs={"class": "form-input"}),
        "cool_skill": forms.TextInput(attrs={"class": "form-input"}),
        "personal_qualities": forms.Textarea(attrs={"class": "form-input"}),
        "personal_weakness": forms.Textarea(attrs={"class": "form-input"}),
        "motivation": forms.Textarea(attrs={"class": "form-input"}),
        "nigth_shifts": forms.CheckboxInput(attrs={"class": "form-checkbox"}),
        "subscribe": forms.CheckboxInput(attrs={"class": "form-checkbox"}),
    }


class AdminForm(ParticipantForm):
    """
    This form is used to create an admin.
    """

    model = Admin
    fields = "__all__"
    exclude = ParticipantForm.Meta.exclude
    labels = {
        **ParticipantForm.Meta.labels,
    }
    help_texts = {
        **ParticipantForm.Meta.help_texts,
    }
    widgets = {
        **ParticipantForm.Meta.widgets,
    }
