from rest_framework import generics
from rest_framework.exceptions import NotFound
from .models import *
from .serializers import *
from rest_framework.generics import ListAPIView, RetrieveAPIView

# ============================
# 📘 READING TEST VIEWS
# ============================

# Reading testlar ro‘yxati
class ReadingTestListView(ListAPIView):
    queryset = ReadingTest.objects.all()
    serializer_class = ReadingTestSerializer

# Reading testdagi barcha passage lar ro‘yxati
class ReadingTestPassageListView(ListAPIView):
    serializer_class = PassageSerializer

    def get_queryset(self):
        test_id = self.kwargs['test_id']
        return Passage.objects.filter(test_id=test_id).order_by('order')

# Faqat bitta passage (test_id va order bo‘yicha)
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

class SpeakingTestListView(ListAPIView):
    queryset = SpeakingTest.objects.all()
    serializer_class = SpeakingTestSerializer


# ============================
# ✍️ WRITING TEST VIEWS
# ============================

class WritingTestListView(ListAPIView):
    queryset = WritingTest.objects.all()
    serializer_class = WritingTestSerializer


# ============================
# 🎧 LISTENING TEST VIEWS
# ============================

# Listening testlar ro'yxati
class ListeningTestListView(ListAPIView):
    queryset = ListeningTest.objects.all()
    serializer_class = ListeningTestSerializer

# Sectiondagi barcha savollarni chiqarish (test_id va section_number orqali)
class ListeningSectionDetailView(RetrieveAPIView):
    serializer_class = ListeningSectionSerializer

    def get_object(self):
        test_id = self.kwargs['test_id']
        section_number = self.kwargs['section_number']
        try:
            return AudioSection.objects.get(test__id=test_id, section_number=section_number)
        except AudioSection.DoesNotExist:
            raise NotFound("Section not found.")
