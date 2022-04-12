from django.urls import path, include
from BICAPweb import views as BICAPviews

urlpatterns = [
    path("api/", include('BICAPweb.api.urls'))
]
