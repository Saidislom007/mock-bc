from django.urls import path
from .views import *

urlpatterns = [
    # === MOCKS (Admin uchun hamma Mock larni ko‘rish) ===
    path('api/mock/', MockListView.as_view(), name="mock-list"),

    # === Reading Tests (faqat active mock) ===
    path('api/mocks/reading/', ReadingTestListView.as_view(), name='mock-reading-tests'),
    path('api/mocks/reading/<int:test_id>/passages/', ReadingTestPassageListView.as_view(), name='mock-reading-passages'),
    path('api/mocks/reading/<int:test_id>/passage/<int:order>/', ReadingTestSinglePassageView.as_view(), name='mock-reading-single-passage'),

    # === Speaking Tests (faqat active mock) ===
    path('api/mocks/speaking/', SpeakingTestListView.as_view(), name='mock-speaking-tests'),

    # === Writing Tests (faqat active mock) ===
    path('api/mocks/writing/', WritingTestListView.as_view(), name='mock-writing-tests'),

    # === Listening Tests (faqat active mock) ===
    path('api/mocks/listening/', ListeningTestListView.as_view(), name='mock-listening-tests'),
    path('api/mocks/listening/<int:test_id>/section/<int:section_number>/', ListeningSectionDetailView.as_view(), name='mock-listening-section-detail'),
]
