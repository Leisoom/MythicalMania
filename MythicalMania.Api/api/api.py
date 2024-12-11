from django.http import JsonResponse
from ninja import NinjaAPI

api = NinjaAPI()

@api.get("/hello")
def hello(request):
    return "Hello world"

@api.get("/")
def index(request):
    return JsonResponse({"detail": "Not Found"}, status=404);