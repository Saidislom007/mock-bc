from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.exceptions import NotFound
from django.utils import timezone

from .models import *
from .serializers import *


# ============================
# 🟢 MOCK VIEWS (faqat bugungi active bo'lganlar)
# ============================
class ActiveMockMixin:
    """Faqat active va bugungi Mock ni olish"""
    def get_active_mock(self):
        today = timezone.now().date()
        mock = (
            Mock.objects
            .filter(status="active", exam_date=today)
            .prefetch_related(
                # 📘 Reading
                "reading_tests__passages__questions",
                # 🎧 Listening
                "listening_tests__sections__questions",
                # 🎙️ Speaking
                "speaking_tests__part1__questions",   # Part 1 + savollari
                "speaking_tests__part2",              # Part 2 cue card
                "speaking_tests__part3__questions",   # Part 3 + savollari
                # ✍️ Writing
                "writing_tests__task1",
                "writing_tests__task2",
            )
            .first()
        )
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
        return Passage.objects.filter(test__id=self.kwargs["test_id"]).order_by("order")


class ReadingTestSinglePassageView(RetrieveAPIView):
    serializer_class = PassageSerializer

    def get_object(self):
        return get_object_or_404(
            Passage,
            test__id=self.kwargs["test_id"],
            order=self.kwargs["order"]
        )


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
        return get_object_or_404(
            AudioSection,
            test__id=self.kwargs["test_id"],
            section_number=self.kwargs["section_number"]
        )
