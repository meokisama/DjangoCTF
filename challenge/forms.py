from django import forms
from django.forms import ModelForm
from .models import Challenge

class DateTimeInput(forms.DateTimeInput):
    input_type = 'datetime-local'

class ChallengeForm(ModelForm):
    class Meta:
        model = Challenge
        fields = '__all__'
        widgets = {
            'date_start' : DateTimeInput(),
            'date_end' : DateTimeInput()
        }