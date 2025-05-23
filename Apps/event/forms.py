from django import forms
from .models import Event

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = '__all__'
        labels = {
            'name': 'Event Name',
            'AppName': 'App Name',
            'description': 'Description',
            'location': 'Location',
            'timezone': 'Timezone',
            'start_date': 'Start Date',
            'end_date': 'End Date',
            'hacker_deadline': 'Hacker Deadline',
            'mentor_deadline': 'Mentor Deadline',
            'volunteer_deadline': 'Volunteer Deadline',
            'sponsor_deadline': 'Sponsor Deadline',
            'domain_link': 'Domain Link',
            'live_link': 'Live Link',
            'x_link': "X Link",
            'facebook_link': "Facebook Link",
            'instagram_link': "Instagram Link",
            'terms_and_conditions_link': "Terms and Conditions Link",
        }
        help_texts = {
            'name': 'Event description',
            'AppName': '',
            'description': '',
            'location': '',
            'timezone': '',
            'start_date': 'Event timings',
            'end_date': '',
            'hacker_deadline': '',
            'mentor_deadline': '',
            'volunteer_deadline': '',
            'sponsor_deadline': '',
            'domain_link': 'Links',
            'live_link': '',
            'x_link': '',
            'facebook_link': '',
            'instagram_link': '',
            'terms_and_conditions_link': '',
        }

        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local','class': 'form-input'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local','class': 'form-input'}),
            'hacker_deadline': forms.DateTimeInput(attrs={'type': 'datetime-local','class': 'form-input'}),
            'mentor_deadline': forms.DateTimeInput(attrs={'type': 'datetime-local','class': 'form-input'}),
            'volunteer_deadline': forms.DateTimeInput(attrs={'type': 'datetime-local','class': 'form-input'}),
            'sponsor_deadline': forms.DateTimeInput(attrs={'type': 'datetime-local','class': 'form-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if field.widget is not None:
                field.widget.attrs.update({'class': 'form-input'})
