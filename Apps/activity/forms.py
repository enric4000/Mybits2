from django import forms
from .models import Activity

class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = '__all__'
        exclude = ['id', 'event', 'hacker_participants', 'mentor_participants', 'sponsor_participants', 'volunteer_participants', 'admin_participants']
        labels = {
            'name': 'Activity name',
            'type': 'Activity Type',
            'description': 'Activity Description',
            'start_date': 'Start Date',
            'end_date': 'End Date',
        }
        help_texts = {
            'name': 'Activity creation',
        }
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local','class': 'form-input'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local','class': 'form-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if field.widget is not None:
                field.widget.attrs.update({'class': 'form-input'})
