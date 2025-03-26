from django.urls import path
from .views import home, create_student, student_detail, get_student, api_ui

urlpatterns = [
    path('', home, name='home'),
    path('student', create_student, name='create_student'),
    path('student/<int:student_id>', student_detail, name='student_detail'),
    path('students', get_student),
    path('students/<int:student_id>', get_student),
    path('api-ui', api_ui),
]
