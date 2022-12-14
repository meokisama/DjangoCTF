from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from django.core.files.storage import FileSystemStorage

from .forms import ChallengeForm, QuizzForm
from .forms import Challenge, Quizz, Hint

# Create your views here.


def viewChallenge(request):
    challenges=Challenge.objects.all().filter(owner=request.user)

    context={'challenges':challenges}
    return render(request, 'challenge.html',context)


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
                name=name,
                owner=str(request.user),
                date_start=date_start,
                date_end=date_end,
                description=description
            )
            challenge.save()
            # print(form)
            return redirect(f'create_challenge_quizz/{challenge.id}')

    context = {'form': form}
    return render(request, 'create_challenge.html', context)


@login_required(login_url='login')
def create_challenge_quizz(request, pk):
    challenge = Challenge.objects.get(id=pk)
    name = challenge.name
    context = {'name': name}
    form = QuizzForm()

    if request.method == 'POST':
        form=QuizzForm(request.POST,request.FILES)
        if form.is_valid():
            names = request.POST.getlist('name')
            questions = request.POST.getlist('question')
            answers = request.POST.getlist('answer')
            points = request.POST.getlist('point')
            hints = request.POST.getlist('hint')
            hint_points = request.POST.getlist('hint_point')
            quizz_ids = request.POST.getlist('quizz_id')
            files = request.FILES.getlist('file_content')
            dict_id =  {}
            count=1
            for name, question, answer, point, file in zip(names, questions, answers, points, files):
                quizz = Quizz.objects.create(
                    challenge_id=pk,
                    name=name,
                    question=question,
                    answer=answer,
                    point=point,
                    file_content=file
                )
                quizz.save()
                

                dict_id["quizz-card"+str(count)]=quizz.id
                count=count+1

            for content, hint_point,quizz_id in zip(hints,hint_points,quizz_ids):
                temp=dict_id.get(quizz_id)
                quizz_id=temp
                # print(quizz_id)
                hint = Hint.objects.create(
                    quizz_id=quizz_id,
                    content=content,
                    point=hint_point
                )
                hint.save()
            return redirect(viewChallenge)
        


    context = {'form': form}
    return render(request, 'create_challenge_quizz.html', context)

@login_required(login_url='login')
def display_quizzes(request, pk):
    challenge = Challenge.objects.get(id=pk)
    quizzes=Quizz.objects.all().filter(challenge_id=pk).values('id','name','question','answer','point','file_content')

    hint_counts=[]

    for quizz in quizzes:
        id=quizz['id']
        hint_count=Hint.objects.all().filter(quizz_id=id).count()
        hint_counts.append(hint_count)

    print(quizzes)

    context={'challenge':challenge,'quizzes':quizzes,'hintCounts':hint_counts}

    return render(request, 'display_quizzes.html',context)
