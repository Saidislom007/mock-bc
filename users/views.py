from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import User, TestResult, OverallScore
from .serializers import UserSerializer, TestResultSerializer, OverallScoreSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404


class UserViewSet(viewsets.ModelViewSet):
    """
    Foydalanuvchilar ro'yxati, qo'shish, tahrirlash va o'chirish uchun.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class TestResultViewSet(viewsets.ModelViewSet):
    """
    Test natijalarini yaratish, ko'rish, tahrirlash, o'chirish uchun.
    """
    queryset = TestResult.objects.all()
    serializer_class = TestResultSerializer

    @action(detail=False, methods=['get'], url_path='by-user-info')
    def get_by_user_info(self, request):
        """
        Ism, familiya va otasining ismi orqali foydalanuvchining test natijalarini olish.
        GET parametrlari: name, last_name, middle_name
        """
        name = request.query_params.get('name')
        last_name = request.query_params.get('last_name')
        middle_name = request.query_params.get('middle_name')

        if not all([name, last_name, middle_name]):
            return Response(
                {'error': 'name, last_name, and middle_name are required.'},
                status=400
            )

        user = get_object_or_404(User, name=name, last_name=last_name, middle_name=middle_name)
        results = TestResult.objects.filter(user=user)
        serializer = self.get_serializer(results, many=True)
        return Response(serializer.data)


class OverallScoreViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Overall score faqat ko‘rish uchun (read-only). Bu qiymatlar avtomatik hisoblanadi.
    """
    queryset = OverallScore.objects.all()
    serializer_class = OverallScoreSerializer
