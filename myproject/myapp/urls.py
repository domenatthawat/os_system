from django.urls import path
from .views import home
from .views import create_student

urlpatterns = [
    path('', home, name='home'),
    path('student', create_student, name='create_student'),
]
