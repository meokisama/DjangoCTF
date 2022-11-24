from django.forms import ModelForm
from .models import Challenge
class ChallengeForm(ModelForm):
    class Meta:
        model = Challenge
        fields = '__all__'