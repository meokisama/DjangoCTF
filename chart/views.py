from django.shortcuts import render
from community.models import Topic, Post
from challenge.models import Challenge

# Create your views here.
def chart(request):
    topics = Topic.objects.all()
    data_post = []
    data_challenge = []

    for topic in topics:
        data_post.append(topic.post_set.all().count())
        # data_challenge.append(topic.challenge_set.all().count())
    
    challenges = Challenge.objects.all()

    html_challenges=Challenge.objects.get(id=42)

    data_challenge = [5, 4, 1, 3, 1]
    context = {'topics':topics, 'data_post':data_post, 'data_challenge':data_challenge}
    return render(request, 'chart/chart.html', context)