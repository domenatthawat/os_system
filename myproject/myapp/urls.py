from django.urls import path
from .views import home
from .views import create_student, update_student

urlpatterns = [
    path('', home, name='home'),
    path('student', create_student, name='create_student'),
    path('student/<int:student_id>', update_student, name='update_student'),
]
