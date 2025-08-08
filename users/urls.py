from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, TestResultViewSet, OverallScoreViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'test-results', TestResultViewSet, basename='test-result')
router.register(r'overall-scores', OverallScoreViewSet, basename='overallscore')


urlpatterns = [
    path('', include(router.urls)),
]
