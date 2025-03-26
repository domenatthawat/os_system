import json
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import Student
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated


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
    
# @csrf_exempt
# @require_http_methods(["PUT"])
# def update_student(request, student_id):
#     try:
#         data = json.loads(request.body)
#         try:
#             student = Student.objects.get(studentID=student_id)
#         except Student.DoesNotExist:
#             return JsonResponse({"error": "Student not found"}, status=404)
        
#         student.studentName = data.get("studentName", student.studentName)
#         student.course = data.get("course", student.course)
#         student.presentDate = data.get("presentDate", student.presentDate)
#         student.save()
        
#         return JsonResponse({
#             "message": "Student updated successfully",
#             "studentID": student.studentID,
#             "studentName": student.studentName,
#             "course": student.course,
#             "presentDate": str(student.presentDate)
#         }, status=200)
#     except Exception as e:
#         return JsonResponse({"error": str(e)}, status=500)
    
# @csrf_exempt
# @require_http_methods(["DELETE"])
# def delete_student(request, student_id):
    try:
        if student_id not in STUDENTS:
            return JsonResponse({"error": "Student not exists"}, status=404)
        del STUDENTS[student_id]
        return JsonResponse({"message": "Student deleted successfully"}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
def student_detail(request, student_id):
    if request.method == "PUT":
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
    
    elif request.method == "DELETE":
        try:
            student = Student.objects.get(studentID=student_id)
            student.delete()
            return JsonResponse({"message": "Student deleted successfully"}, status=200)
        except Student.DoesNotExist:
            return JsonResponse({"error": "Student not exists"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)

@require_http_methods(["GET"])
def get_student(request, student_id=None):
    if student_id:
        try:
            student = Student.objects.get(pk=student_id)
            data = {
                "studentID": student.studentID,
                "studentName": student.studentName,
                "course": student.course,
                "presentDate": student.presentDate
            }
            return JsonResponse(data, status=200)
        except Student.DoesNotExist:
            return JsonResponse({"error": "Student not exists"}, status=404)
    else:
        students = Student.objects.all().values()
        return JsonResponse(list(students), safe=False)


def api_ui(request):
    return render(request, 'API.html')

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_protected_students(request):
    students = Student.objects.all().values()
    return JsonResponse(list(students), safe=False)
