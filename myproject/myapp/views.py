from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist

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