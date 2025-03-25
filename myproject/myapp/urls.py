from django.urls import path
from .views import home
from .views import create_student, student_detail

urlpatterns = [
    path('', home, name='home'),
    path('student', create_student, name='create_student'),
    path('student/<int:student_id>', student_detail, name='student_detail'),
]
