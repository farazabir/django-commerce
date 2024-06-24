from django.urls import include, path

from ambassador.views import LinkAPIView, ProductBackendAPIView, ProductFrontendAPIView, RankingAPIView, StatsAPIView

urlpatterns = [
    path('', include('common.urls')),
    path('product/frontend', ProductFrontendAPIView.as_view()),
    path('product/backend', ProductBackendAPIView.as_view()),
    path('links', LinkAPIView.as_view()),
    path('stats', StatsAPIView.as_view()),
    path('rankings', RankingAPIView.as_view()),

]
