import json
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

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
        
        if student_id in STUDENTS:
            return JsonResponse({"error": "Student already exists"}, status=409)
        
        STUDENTS[student_id] = {
            "studentName": data.get("studentName"),
            "course": data.get("course"),
            "presentDate": data.get("presentDate")
        }
        
        return JsonResponse({
            "message": "Student created successfully",
            "studentID": student_id,
            "studentName": data.get("studentName"),
            "course": data.get("course"),
            "presentDate": data.get("presentDate")
        }, status=201)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)