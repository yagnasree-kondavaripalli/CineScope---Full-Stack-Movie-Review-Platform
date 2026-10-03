from django.contrib import admin
from django.urls import include, path
from django.http import JsonResponse


def health(request):
    return JsonResponse({"status": "ok", "service": "CineScope API"})


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/health/", health),
    path("api/movies/", include("movies.urls")),
    path("api/auth/", include("users.urls")),
    path("api/", include("reviews.urls")),
]
