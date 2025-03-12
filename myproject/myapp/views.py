import json
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import Student

def home(request):
    return JsonResponse({"message": "Welcome to My Django App!"})


def safe_view(request):
    try:
        obj = MyModel.objects.get(id=1)
        return JsonResponse({"data": obj.name})
    except ObjectDoesNotExist:
        return JsonResponse({"error": "Object not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    
STUDENTS = {}

@csrf_exempt
@require_http_methods(["POST"])
def create_student(request):
    try:
        data = json.loads(request.body)
        student_id = data.get("studentID")
        
        if Student.objects.filter(studentID=student_id).exists():
            return JsonResponse({"error": "Student already exists"}, status=409)
        
        student = Student.objects.create(
            studentID=student_id,
            studentName=data.get("studentName"),
            course=data.get("course"),
            presentDate=data.get("presentDate")
        )
        
        return JsonResponse({
            "message": "Student created successfully",
            "studentID": student.studentID,
            "studentName": student.studentName,
            "course": student.course,
            "presentDate": str(student.presentDate)
        }, status=201)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    
@csrf_exempt
@require_http_methods(["PUT"])
def update_student(request, student_id):
    try:
        data = json.loads(request.body)
        try:
            student = Student.objects.get(studentID=student_id)
        except Student.DoesNotExist:
            return JsonResponse({"error": "Student not found"}, status=404)
        
        student.studentName = data.get("studentName", student.studentName)
        student.course = data.get("course", student.course)
        student.presentDate = data.get("presentDate", student.presentDate)
        student.save()
        
        return JsonResponse({
            "message": "Student updated successfully",
            "studentID": student.studentID,
            "studentName": student.studentName,
            "course": student.course,
            "presentDate": str(student.presentDate)
        }, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)