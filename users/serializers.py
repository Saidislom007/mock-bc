from rest_framework import serializers
from .models import User, TestResult, OverallScore


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class OverallScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = OverallScore
        # Biz test_result ni chiqarishni xohlamaymiz, faqat band scoreni beramiz
        fields = [
            'reading_band',
            'listening_band',
            'speaking_band',
            'writing_band',
            'overall_band'
        ]
        read_only_fields = fields  # Barchasi readonly, avtomatik hisoblanadi


class TestResultSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    overall_score = OverallScoreSerializer(read_only=True)

    class Meta:
        model = TestResult
        fields = '__all__'
