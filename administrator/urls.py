from django.contrib import admin
from django.urls import include, path

from administrator.views import AmbassadorAPIView, LinkApiView, OrderAPIView, ProductGenericAPIView

urlpatterns = [
    path('', include('common.urls')),
    path('ambassadors', AmbassadorAPIView.as_view()),
    path('products', ProductGenericAPIView.as_view()),
    path('products/<str:pk>', ProductGenericAPIView.as_view()),
    path('users/<str:pk>/links', LinkApiView.as_view()),
    path('orders', OrderAPIView.as_view()),
]
