from django import forms
from .models import Luggage, Warehouse

class WarehouseForm(forms.ModelForm):
    class Meta:
        model = Warehouse
        fields = '__all__'
        exclude = ['id', 'event', 'luggage']
        labels = {
            'name': 'Warehouse name',
            'columns': 'Columns',
            'rows': 'Rows',
        }
        help_texts = {
            'name': 'Warehouse creation'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if field.widget is not None:
                field.widget.attrs.update({'class': 'form-input'})

class LuggageForm(forms.ModelForm):
    class Meta:
        model = Luggage
        fields = '__all__'
        exclude = ['id', 'warehouse', 'owner']
        labels = {
            'name': 'Luggage',
            'description': 'Description',
            'row_position': 'Row Position',
            'column_position': 'Column Position',
            'image': 'Image',
        }
        help_texts = {
            'name': 'Lugagge creation'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if field.widget is not None:
                field.widget.attrs.update({'class': 'form-input'})
