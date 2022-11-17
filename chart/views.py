from django.shortcuts import render
from community.models import Topic, Post

# Create your views here.
def chart(request):
    topics = Topic.objects.all()
    data_post = []
    data_challenge = []
    for topic in topics:
        data_post.append(topic.post_set.all().count())
        # data_challenge.append(topic.challenge_set.all().count())
    data_challenge = [5, 4, 1, 3]
    context = {'topics':topics, 'data_post':data_post, 'data_challenge':data_challenge}
    return render(request, 'chart/chart.html', context)