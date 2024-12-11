from django.http import JsonResponse
from django.urls import path, re_path

from . import views
from .api import api

urlpatterns = [
    path("", api.urls),
    re_path(r"^.*$", lambda request: JsonResponse({"detail": "Not Found"}, status=404))
]