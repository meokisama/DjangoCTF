from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from django.core.files.storage import FileSystemStorage

from .forms import ChallengeForm, QuizzForm, AnswerForm
from .forms import Challenge, Quizz, Hint, Answer

from community.models import User, Note

# Create your views here.


def viewChallenge(request):
    challenges={}
    if request.user.is_superuser:
        challenges=Challenge.objects.all().filter(owner=request.user)
        is_super='yes'
    else:
        is_super='no'

    print(is_super)

    context={'challenges':challenges,'is_super':is_super}
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
            return redirect(create_challenge_quizz,pk=challenge.id)
            # return redirect(f'create_challenge_quizz/{challenge.id}/')

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
            # print(names)
            # print(files)
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

    context={'challenge':challenge,'quizzes':quizzes,'hintCounts':hint_counts}

    return render(request, 'display_quizzes.html',context)

@login_required(login_url='login')
def edit_quizz(request,pk,pk1):
    quizz=Quizz.objects.get(id=pk1)

    form = QuizzForm()
    
    hints=Hint.objects.filter(quizz_id=pk1).values('content','point')

    if request.method == 'POST':
        form=QuizzForm(request.POST,request.FILES,instance=quizz)
        # print(form)
        if form.is_valid():
            Hint.objects.filter(quizz_id=pk1).delete()
            hints = request.POST.getlist('hint')
            hint_points = request.POST.getlist('hint_point')
            # print(hints)

            for content, hint_point in zip(hints,hint_points):
                hint = Hint.objects.create(
                    quizz_id=pk1,
                    content=content,
                    point=hint_point
                )
                hint.save()

            form.save()
            return redirect(display_quizzes,pk=pk)
        
        # form=QuizzForm(request.POST)
        # hintss = request.POST.getlist('hint')
        # hint_points = request.POST.getlist('hint_point')
        # print(hintss)
        
    
    context={'form':form,'quizz':quizz,'challenge_id':pk,'hints':hints}
    return render(request, 'edit_a_quizz.html',context)



def join_challenge(request, pk):
    challenge = Challenge.objects.get(id=pk)

    creator = User.objects.get(username=challenge.owner)
    creator_name=creator.name

    context={'challenge':challenge,'creator_name':creator_name}
    return render(request, 'join_challenge.html',context)

def register_challenge(request, pk):
    challenge = Challenge.objects.get(id=pk)

    creator = User.objects.get(username=challenge.owner)
    creator_name=creator.name

    try:
        obj=Note.objects.get(challenge_id=challenge.id)
        registered='yes'
    except Note.DoesNotExist:
        registered='no'

    if request.method == 'POST':
        _content=challenge.name+" has started. Join us now!"
        note = Note.objects.create(
            user=request.user,
            date=challenge.date_start,
            content=_content,
            challenge_id=challenge.id
        )
        note.save()
        return redirect('upcoming')

    # print(creator_name)
    context={'challenge':challenge,'creator_name':creator_name,'registered':registered}
    return render(request, 'register_challenge.html',context)

def expired_challenge(request, pk):
    challenge = Challenge.objects.get(id=pk)

    creator = User.objects.get(username=challenge.owner)
    creator_name=creator.name

    context={'challenge':challenge,'creator_name':creator_name}
    return render(request, 'expired_challenge.html',context)

def play_challenge(request, pk):
    challenge = Challenge.objects.get(id=pk)
    quizzes=Quizz.objects.all().filter(challenge_id=pk).values('id','name','question','answer','point','file_content')

    quizz_status={}

    score=0

    for quizz in quizzes:
        try:
            obj = Answer.objects.get(quizz_id=quizz['id'])
            quizz_status[quizz['id']]='yes'
            score+=obj.point
        except Answer.DoesNotExist:
            quizz_status[quizz['id']]='no'
            pass
    
    print(quizz_status)

    context={'challenge':challenge,'quizzes':quizzes,'quizz_status':quizz_status,'score':score}
    return render(request, 'play_challenge.html',context)

def play_challenge_quizz(request, pk, pk1):
    challenge = Challenge.objects.get(id=pk)
    quizz = Quizz.objects.get(id=pk1)
    hints = Hint.objects.filter(quizz_id=quizz.id)

    _point=0

    if request.method == 'POST':
            _answer = request.POST.get('answer')
            minus_point=request.POST.get('minus-point')
            # print('begin')
            # print(minus_point)
            if _answer==quizz.answer:
                _point=quizz.point-int(minus_point)
            else:
                _point=0

            try:
                obj = Answer.objects.get(quizz_id=quizz.id)
                _point=int(75*int(_point)/100)
                obj.point=_point
                obj.save()
            except Answer.DoesNotExist:
                answer_obj=Answer.objects.create(
                    challenge_id=challenge.id,
                    username=request.user.username,
                    quizz_id=quizz.id,
                    answer=_answer,
                    point=_point
                )
                answer_obj.save()

            return redirect(play_challenge,pk=pk)

    # print(hints)

    context={'challenge':challenge,'quizz':quizz,'hints':hints}
    return render(request, 'play_challenge_quizz.html',context)