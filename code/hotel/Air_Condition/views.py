from django.shortcuts import render
from .models import Room
# Create your views here.


# 首页
def index(request):

    # render函数：载入模板，并返回context对象
    return render(request, 'Air_Condition/index.html')


def room1(request):
    room = Room.objects.filter(room_id=1)
    return render(request, 'Air_Condition/index', context={'room': room})
