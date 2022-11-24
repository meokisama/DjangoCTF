from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .forms import ChallengeForm

# Create your views here.

def challenge(request):
    return render(request, 'challenge.html')

@login_required(login_url='login')
def create_challenge(request):

    form = ChallengeForm()

    context={'form':form}
    return render(request,'create_challenge.html',context)