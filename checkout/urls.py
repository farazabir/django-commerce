from django.urls import include, path

from checkout.views import LinkAPIView


urlpatterns = [
    path('link/<str:code>', LinkAPIView.as_view())
]
