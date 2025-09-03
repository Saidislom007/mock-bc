from django.urls import path
from .views import *

urlpatterns = [
    # ============================
    # 🟢 MOCKS (Admin uchun)
    # ============================
    path("api/mocks/", MockListView.as_view(), name="mocks-list"),

    # ============================
    # 📘 READING (faqat active mock)
    # ============================
    path("api/mocks/reading/", ReadingTestListView.as_view(), name="mocks-reading-list"),
    path("api/mocks/reading/<int:test_id>/passages/", ReadingTestPassageListView.as_view(), name="mocks-reading-passages"),
    path("api/mocks/reading/<int:test_id>/passage/<int:order>/", ReadingTestSinglePassageView.as_view(), name="mocks-reading-single-passage"),

    # ============================
    # 🎙️ SPEAKING (faqat active mock)
    # ============================
    path("api/mocks/speaking/", SpeakingTestListView.as_view(), name="mocks-speaking-list"),

    # ============================
    # ✍️ WRITING (faqat active mock)
    # ============================
    path("api/mocks/writing/", WritingTestListView.as_view(), name="mocks-writing-list"),

    # ============================
    # 🎧 LISTENING (faqat active mock)
    # ============================
    path("api/mocks/listening/", ListeningTestListView.as_view(), name="mocks-listening-list"),
    path("api/mocks/listening/<int:test_id>/section/<int:section_number>/", ListeningSectionDetailView.as_view(), name="mocks-listening-section-detail"),
]
