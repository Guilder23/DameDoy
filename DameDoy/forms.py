from django import forms
from .models import Material

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result

class MaterialForm(forms.ModelForm):
    archivos = MultipleFileField(
        required=False,
        widget=MultipleFileInput(attrs={
            'class': 'form-control',
            'accept': '.pdf,.doc,.docx,.xls,.xlsx,.ppt,.pptx,.zip,.rar,.txt'
        })
    )

    class Meta:
        model = Material
        fields = ['titulo', 'tipo', 'facultad', 'carrera', 'materia', 
                 'docente', 'descripcion', 'precio', 'imagen']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field != 'archivos':
                self.fields[field].widget.attrs.update({
                    'class': 'form-control',
                    'placeholder': self.fields[field].label
                })