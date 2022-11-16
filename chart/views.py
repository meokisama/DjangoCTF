from django.shortcuts import render
from community.models import Topic

# Create your views here.
def chart(request):
    topics = Topic.objects.all()
    context = {'topics':topics}
    return render(request, 'chart/chart.html', context)