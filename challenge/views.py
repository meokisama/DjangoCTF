from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import ChallengeForm
from .forms import Challenge

# Create your views here.

def challenge(request):
    return render(request, 'challenge.html')

@login_required(login_url='login')
def create_challenge(request):

    form = ChallengeForm()
    if request.method == 'POST':
        form = ChallengeForm(request.POST)
        if form.is_valid():
            name = request.POST.get('name')
            date_start = request.POST.get('date_start')
            date_end = request.POST.get('date_end')
            description = request.POST.get('description')

            challenge = Challenge.objects.create(
                name = name,
                date_start = date_start,
                date_end = date_end,
                description = description
            )
            challenge.save()
            print(challenge.id)
            return redirect(f'create_challenge_quizz/{challenge.id}')

    context={'form':form}
    return render(request,'create_challenge.html',context)

@login_required(login_url='login')
def create_challenge_quizz(request, pk):
    challenge = Challenge.objects.get(id=pk)
    name = challenge.name
    context= {'name':name}
    return render(request,'create_challenge_quizz.html',context)