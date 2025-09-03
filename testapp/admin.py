from django.contrib import admin, messages
from django.utils import timezone
from django.core.exceptions import ValidationError
from .models import (
    Mock,
    # Reading
    ReadingTest, Passage, ReadingQuestion, ReadingTable, ReadingTableRow, ReadingTableAnswer,
    # Speaking
    SpeakingTest, SpeakingPart1Question, SpeakingPart2CueCard, SpeakingPart3Question,
    # Writing
    WritingTest, WritingTask1, WritingTask2,
    # Listening
    ListeningTest, AudioSection, ListeningQuestion,
    ListeningTable, ListeningTableRow, ListeningTableAnswer
)


# =========================================
# MOCK ADMIN
# =========================================
@admin.register(Mock)
class MockAdmin(admin.ModelAdmin):
    list_display = ("title", "number", "status", "exam_date", "is_open_today", "created_at")
    search_fields = ("title",)
    list_filter = ("status", "exam_date", "created_at")
    filter_horizontal = ("reading_tests", "listening_tests", "speaking_tests", "writing_tests")
    ordering = ["-created_at"]
    readonly_fields = ("created_at",)

    def save_model(self, request, obj, form, change):
        # exam date o‘tgan bo‘lsa -> inactive
        if obj.exam_date and obj.exam_date < timezone.now().date():
            obj.status = "inactive"

        # faqat bitta active qolsin
        if obj.status == "active":
            Mock.objects.exclude(pk=obj.pk).filter(status="active").update(status="inactive")

        try:
            obj.full_clean()
            super().save_model(request, obj, form, change)
        except ValidationError as e:
            self.message_user(request, f"Xato: {e}", level=messages.ERROR)


# =========================================
# READING ADMIN
# =========================================
class QuestionInline(admin.TabularInline):
    model = ReadingQuestion
    extra = 1
    show_change_link = True
    fields = (
        'question_number', 'question_type', 'question_text',
        'options', 'diagram_labels', 'paragraph_mapping',
        'correct_answer'
    )


class PassageInline(admin.StackedInline):
    model = Passage
    extra = 1
    show_change_link = True


@admin.register(ReadingTest)
class ReadingTestAdmin(admin.ModelAdmin):
    list_display = ['title', 'duration_minutes', 'created_at']
    readonly_fields = ['created_at']
    inlines = [PassageInline]


@admin.register(Passage)
class PassageAdmin(admin.ModelAdmin):
    list_display = ['title', 'test', 'order']
    list_filter = ['test']
    search_fields = ['title', 'text']
    inlines = [QuestionInline]


@admin.register(ReadingQuestion)
class ReadingQuestionAdmin(admin.ModelAdmin):
    list_display = ['question_number', 'question_type', 'passage', 'linked_question_display']
    list_filter = ['question_type', 'passage__test']
    search_fields = ['question_text', 'correct_answer']
    ordering = ['passage', 'question_number']

    def linked_question_display(self, obj):
        return obj.linked_question_id or "-"
    linked_question_display.short_description = "Linked Q"


class ReadingTableRowInline(admin.TabularInline):
    model = ReadingTableRow
    extra = 1
    fields = ['order', 'row_data']


class ReadingTableAnswerInline(admin.TabularInline):
    model = ReadingTableAnswer
    extra = 1
    fields = ['number', 'correct_answer']


@admin.register(ReadingTable)
class ReadingTableAdmin(admin.ModelAdmin):
    list_display = ['question']
    search_fields = ['question__question_text']
    inlines = [ReadingTableRowInline, ReadingTableAnswerInline]


# =========================================
# SPEAKING ADMIN
# =========================================
class SpeakingPart1Inline(admin.TabularInline):
    model = SpeakingPart1Question
    extra = 1


class SpeakingPart2Inline(admin.StackedInline):
    model = SpeakingPart2CueCard
    extra = 1
    max_num = 1


class SpeakingPart3Inline(admin.TabularInline):
    model = SpeakingPart3Question
    extra = 1


@admin.register(SpeakingTest)
class SpeakingTestAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at']
    readonly_fields = ['created_at']
    inlines = [SpeakingPart1Inline, SpeakingPart2Inline, SpeakingPart3Inline]


# =========================================
# WRITING ADMIN
# =========================================
class WritingTask1Inline(admin.StackedInline):
    model = WritingTask1
    extra = 1
    max_num = 1


class WritingTask2Inline(admin.StackedInline):
    model = WritingTask2
    extra = 1
    max_num = 1


@admin.register(WritingTest)
class WritingTestAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at']
    readonly_fields = ['created_at']
    inlines = [WritingTask1Inline, WritingTask2Inline]


# =========================================
# LISTENING ADMIN
# =========================================
class ListeningQuestionInline(admin.TabularInline):
    model = ListeningQuestion
    extra = 1
    fields = (
        'question_number', 'question_type', 'instruction',
        'question_text', 'options', 'correct_answer'
    )
    show_change_link = True


class AudioSectionInline(admin.StackedInline):
    model = AudioSection
    extra = 1
    show_change_link = True
    fields = (
        'section_number', 'instruction', 'start_time',
        'end_time', 'audio_file'
    )


@admin.register(ListeningTest)
class ListeningTestAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at']
    readonly_fields = ['created_at']
    search_fields = ['title']
    ordering = ['-created_at']
    inlines = [AudioSectionInline]


@admin.register(AudioSection)
class AudioSectionAdmin(admin.ModelAdmin):
    list_display = ['test', 'section_number', 'audio_file']
    list_filter = ['test']
    search_fields = ['instruction']
    ordering = ['test', 'section_number']
    inlines = [ListeningQuestionInline]


@admin.register(ListeningQuestion)
class ListeningQuestionAdmin(admin.ModelAdmin):
    list_display = ['section', 'question_number', 'question_type', 'linked_question_display', 'has_table']
    list_filter = ['question_type', 'section__test']
    search_fields = ['question_text']
    ordering = ['section', 'question_number']

    def linked_question_display(self, obj):
        return getattr(obj, "linked_question_id", None) or "-"
    linked_question_display.short_description = "Linked Q"

    def has_table(self, obj):
        return hasattr(obj, 'table')
    has_table.boolean = True
    has_table.short_description = 'Table?'


class ListeningTableRowInline(admin.TabularInline):
    model = ListeningTableRow
    extra = 1
    fields = ['order', 'row_data']


class ListeningTableAnswerInline(admin.TabularInline):
    model = ListeningTableAnswer
    extra = 1
    fields = ['number', 'correct_answer']


@admin.register(ListeningTable)
class ListeningTableAdmin(admin.ModelAdmin):
    list_display = ['question']
    search_fields = ['question__question_text']
    inlines = [ListeningTableRowInline, ListeningTableAnswerInline]
