from django import forms
from .models import ProjectPreference, Project

class ProjectPreferenceForm(forms.ModelForm):
    first_choice = forms.ModelChoiceField(
        queryset=Project.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='1. Tercih'
    )
    second_choice = forms.ModelChoiceField(
        queryset=Project.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='2. Tercih'
    )
    third_choice = forms.ModelChoiceField(
        queryset=Project.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='3. Tercih'
    )

    class Meta:
        model = ProjectPreference
        fields = ['first_choice', 'second_choice', 'third_choice']

    def clean(self):
        cleaned_data = super().clean()
        choices = [
            cleaned_data.get('first_choice'),
            cleaned_data.get('second_choice'),
            cleaned_data.get('third_choice')
        ]
        
        if len(set(choices)) != len(choices):
            raise forms.ValidationError('Lütfen farklı projeler seçiniz.') 