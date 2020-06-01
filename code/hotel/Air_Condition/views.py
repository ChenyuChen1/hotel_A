from django.shortcuts import render
# Create your views here.


# 首页
def index(request):

    # render函数：载入模板，并返回context对象
    return render(request, 'Air_Condition/index.html')