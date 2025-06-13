from django import forms
from Apps.project.models import Project, Valoration


class ProjectForm(forms.ModelForm):
    """
    Form for creating and updating projects.
    """
    class Meta:
        model = Project
        fields = '__all__'
        exclude = ['id', 'team']
        labels = {
            'name': 'Project name',
            'description': 'Project description',
            'github_link': 'GitHub link',
            'devpost_link': 'Devpost link',
        }
        help_texts = {
            'name': 'Project',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if field.widget is not None:
                field.widget.attrs.update({'class': 'form-input'})

class ValorationForm(forms.ModelForm):
    """
    Form for creating and updating valuations for projects.
    """
    class Meta:
        model = Valoration
        fields = ['score']
        exclude = ['id', 'admin', 'project']
        labels = {
            'score': 'Valoration score',
        }
        help_texts = {
            'score': 'Make a valoration',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if field.widget is not None:
                field.widget.attrs.update({'class': 'form-input'})
