from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .forms import ChallengeForm
from .forms import Challenge

# Create your views here.

def challenge(request):
    return render(request, 'challenge.html')

@login_required(login_url='login')
def create_challenge(request):

    form = ChallengeForm()
    name = request.POST.get('name')
    date_start = request.POST.get('date_start')
    date_end = request.POST.get('date_end')
    description = request.POST.get('description')
    if request.method == 'POST':
        challenge = Challenge.objects.create(
            name = name,
            date_start = date_start,
            date_end = date_end,
            description = description
        )
        challenge.save()

    context={'form':form}
    return render(request,'create_challenge.html',context)