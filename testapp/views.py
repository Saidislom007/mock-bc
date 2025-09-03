from rest_framework import generics
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from django.utils import timezone

from .models import *
from .serializers import *
from rest_framework.generics import ListAPIView, RetrieveAPIView


# ============================
# 🟢 MOCK VIEWS (faqat bugungi active bo'lganlar)
# ============================
class ActiveMockMixin:
    """Faqat active va bugungi Mock ni olish"""
    def get_active_mock(self):
        today = timezone.now().date()
        mock = Mock.objects.filter(status="active", exam_date=today).first()
        if not mock:
            raise NotFound("Bugungi kunda active mock mavjud emas.")
        return mock


class MockListView(ListAPIView):
    """Admin panel uchun barcha Mock ro'yxati (faqat test uchun)"""
    queryset = Mock.objects.all()
    serializer_class = MockSerializer


# ============================
# 📘 READING TEST VIEWS
# ============================
class ReadingTestListView(ActiveMockMixin, ListAPIView):
    serializer_class = ReadingTestSerializer

    def get_queryset(self):
        mock = self.get_active_mock()
        return mock.reading_tests.all()


class ReadingTestPassageListView(ListAPIView):
    serializer_class = PassageSerializer

    def get_queryset(self):
        test_id = self.kwargs['test_id']
        return Passage.objects.filter(test_id=test_id).order_by('order')


class ReadingTestSinglePassageView(RetrieveAPIView):
    serializer_class = PassageSerializer

    def get_object(self):
        test_id = self.kwargs['test_id']
        order = self.kwargs['order']
        try:
            return Passage.objects.get(test_id=test_id, order=order)
        except Passage.DoesNotExist:
            raise NotFound("Passage not found for this test and order.")


# ============================
# 🎙️ SPEAKING TEST VIEWS
# ============================
class SpeakingTestListView(ActiveMockMixin, ListAPIView):
    serializer_class = SpeakingTestSerializer

    def get_queryset(self):
        mock = self.get_active_mock()
        return mock.speaking_tests.all()


# ============================
# ✍️ WRITING TEST VIEWS
# ============================
class WritingTestListView(ActiveMockMixin, ListAPIView):
    serializer_class = WritingTestSerializer

    def get_queryset(self):
        mock = self.get_active_mock()
        return mock.writing_tests.all()


# ============================
# 🎧 LISTENING TEST VIEWS
# ============================
class ListeningTestListView(ActiveMockMixin, ListAPIView):
    serializer_class = ListeningTestSerializer

    def get_queryset(self):
        mock = self.get_active_mock()
        return mock.listening_tests.all()


class ListeningSectionDetailView(RetrieveAPIView):
    serializer_class = ListeningSectionSerializer

    def get_object(self):
        test_id = self.kwargs['test_id']
        section_number = self.kwargs['section_number']
        try:
            return AudioSection.objects.get(test__id=test_id, section_number=section_number)
        except AudioSection.DoesNotExist:
            raise NotFound("Section not found.")
