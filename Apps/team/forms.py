from django import forms
from .models import Team

class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = '__all__'
        exclude = ['id', 'event', 'members']
        labels = {
            'name': 'Team name',
        }
        help_texts = {
            'name': 'Team creation',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if field.widget is not None:
                field.widget.attrs.update({'class': 'form-input'})
