from django.urls import path
from Air_Condition import views

app_name = 'assets'

urlpatterns = [
    path('index/', views.index, name='index'),
]