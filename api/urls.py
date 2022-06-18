from django.urls import include, path


urlpatterns = [
    path("auth/", include("user.urls")),
    path('', include('tools.urls'))
]
