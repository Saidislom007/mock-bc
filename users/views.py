from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import User, TestResult, OverallScore
from .serializers import UserSerializer, TestResultSerializer, OverallScoreSerializer


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

    @action(detail=False, methods=['post'], url_path='by-user-info')
    def get_by_user_info(self, request):
        """
        Ism, familiya va otasining ismi orqali foydalanuvchining
        test natijalari va overall scoreni olish.
        POST body parametrlari: name, last_name, middle_name
        """
        name = request.data.get('name')
        last_name = request.data.get('last_name')
        middle_name = request.data.get('middle_name')

        if not all([name, last_name, middle_name]):
            return Response(
                {'error': 'name, last_name, and middle_name are required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Foydalanuvchini topamiz
        user = get_object_or_404(
            User, name=name, last_name=last_name, middle_name=middle_name
        )

        # Test natijalari
        results = TestResult.objects.filter(user=user)
        results_serializer = self.get_serializer(results, many=True)

        # Overall score
        overall = OverallScore.objects.filter(user=user).first()
        overall_serializer = OverallScoreSerializer(overall) if overall else None

        return Response({
            "user": {
                "id": user.id,
                "name": user.name,
                "last_name": user.last_name,
                "middle_name": user.middle_name,
            },
            "overall_score": overall_serializer.data if overall else None,
            "test_results": results_serializer.data
        })


class OverallScoreViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Overall score faqat ko‘rish uchun (read-only).
    Foydalanuvchi fullname yuborganida uning barcha band scorelari qaytadi.
    """
    queryset = OverallScore.objects.all()
    serializer_class = OverallScoreSerializer

    @action(detail=False, methods=['post'], url_path='by-user-info')
    def get_by_user_info(self, request):
        """
        Foydalanuvchining fullname orqali uning band scorelarini olish.
        POST body parametrlari: name, last_name, middle_name
        """
        name = request.data.get("name")
        last_name = request.data.get("last_name")
        middle_name = request.data.get("middle_name")

        if not all([name, last_name, middle_name]):
            return Response(
                {"error": "name, last_name, and middle_name are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Userni topamiz
        user = get_object_or_404(
            User, name=name, last_name=last_name, middle_name=middle_name
        )

        # OverallScore ni olamiz
        overall = get_object_or_404(OverallScore, user=user)
        serializer = self.get_serializer(overall)

        return Response({
            "user": {
                "id": user.id,
                "name": user.name,
                "last_name": user.last_name,
                "middle_name": user.middle_name,
            },
            "band_scores": {
                "reading": serializer.data.get("reading_band"),
                "listening": serializer.data.get("listening_band"),
                "speaking": serializer.data.get("speaking_band"),
                "writing": serializer.data.get("writing_band"),
            },
            "overall_band": serializer.data.get("overall_band"),
        })
