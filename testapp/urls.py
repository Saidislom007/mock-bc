from django.urls import path
from .views import *

urlpatterns = [
    # === Reading Tests ===
    path('api/reading-tests/', ReadingTestListView.as_view(), name='reading-tests'),
    path('api/reading-tests/<int:test_id>/passages/', ReadingTestPassageListView.as_view(), name='reading-test-passages'),
    path('api/reading-tests/<int:test_id>/passage/<int:order>/', ReadingTestSinglePassageView.as_view(), name='reading-test-single-passage'),

    # === Speaking Tests ===
    path('api/speaking-tests/', SpeakingTestListView.as_view(), name='speaking-tests'),

    # === Writing Tests ===
    path('api/writing-tests/', WritingTestListView.as_view(), name='writing-tests'),

    # === Listening Tests ===
    path('api/listening-tests/', ListeningTestListView.as_view(), name='listening-tests'),
    path('api/listening-tests/<int:test_id>/section/<int:section_number>/', ListeningSectionDetailView.as_view(), name='listening-section-detail'),
]
