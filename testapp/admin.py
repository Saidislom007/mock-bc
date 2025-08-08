from django.contrib import admin
from .models import (
    ReadingTest,
    Passage,
    Question,
    SpeakingTest,
    SpeakingPart1Question,
    SpeakingPart2CueCard,
    SpeakingPart3Question,
    ListeningTest, AudioSection, ListeningQuestion,
    ListeningTable, ListeningTableRow, ListeningTableAnswer,
    WritingTest, WritingTask1, WritingTask2
)


# Reading admin components

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1
    show_change_link = True
    fields = (
        'question_number',
        'question_type',
        'question_text',
        'options',
        'summary_text',
        'diagram_labels',
        'paragraph_mapping',
        'correct_answer'
    )

class PassageInline(admin.StackedInline):
    model = Passage
    extra = 1
    show_change_link = True

@admin.register(ReadingTest)
class ReadingTestAdmin(admin.ModelAdmin):
    list_display = ['title', 'duration_minutes', 'created_at']
    inlines = [PassageInline]

@admin.register(Passage)
class PassageAdmin(admin.ModelAdmin):
    list_display = ['title', 'test', 'order']
    list_filter = ['test']
    inlines = [QuestionInline]
    search_fields = ['title', 'text']

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['question_number', 'question_type', 'passage']
    list_filter = ['question_type', 'passage__test']
    search_fields = ['question_text', 'correct_answer']
    ordering = ['passage', 'question_number']


# Speaking admin components

class SpeakingPart1Inline(admin.TabularInline):
    model = SpeakingPart1Question
    extra = 1

class SpeakingPart2Inline(admin.StackedInline):
    model = SpeakingPart2CueCard
    extra = 1
    max_num = 1  # Har bir testda faqat 1ta cue card bo'lishi kerak

class SpeakingPart3Inline(admin.TabularInline):
    model = SpeakingPart3Question
    extra = 1

@admin.register(SpeakingTest)
class SpeakingTestAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at']
    inlines = [SpeakingPart1Inline, SpeakingPart2Inline, SpeakingPart3Inline]

@admin.register(SpeakingPart1Question)
class SpeakingPart1QuestionAdmin(admin.ModelAdmin):
    list_display = ['test', 'question_text']
    search_fields = ['question_text']

@admin.register(SpeakingPart2CueCard)
class SpeakingPart2CueCardAdmin(admin.ModelAdmin):
    list_display = ['test', 'topic']
    search_fields = ['topic', 'description']

@admin.register(SpeakingPart3Question)
class SpeakingPart3QuestionAdmin(admin.ModelAdmin):
    list_display = ['test', 'question_text']
    search_fields = ['question_text']




class WritingTask1Inline(admin.StackedInline):
    model = WritingTask1
    extra = 1
    max_num = 1  # Faqat 1 ta Task 1


class WritingTask2Inline(admin.StackedInline):
    model = WritingTask2
    extra = 1
    max_num = 1  # Faqat 1 ta Task 2


@admin.register(WritingTest)
class WritingTestAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at']
    inlines = [WritingTask1Inline, WritingTask2Inline]


@admin.register(WritingTask1)
class WritingTask1Admin(admin.ModelAdmin):
    list_display = ['test']
    search_fields = ['question_text']


@admin.register(WritingTask2)
class WritingTask2Admin(admin.ModelAdmin):
    list_display = ['test']
    search_fields = ['question_text']

class ListeningQuestionInline(admin.TabularInline):
    model = ListeningQuestion
    extra = 1
    fields = (
        'question_number',
        'question_type',
        'instruction',
        'question_text',
        'options',
        'correct_answer',
    )
    show_change_link = True


class AudioSectionInline(admin.StackedInline):
    model = AudioSection
    extra = 1
    show_change_link = True
    fields = (
        'section_number',
        'instruction',
        'start_time',
        'end_time',
        'audio_file',
    )


@admin.register(ListeningTest)
class ListeningTestAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at']
    readonly_fields = ['created_at']
    inlines = [AudioSectionInline]
    search_fields = ['title']
    ordering = ['-created_at']


@admin.register(AudioSection)
class AudioSectionAdmin(admin.ModelAdmin):
    list_display = ['test', 'section_number', 'audio_file']
    inlines = [ListeningQuestionInline]
    ordering = ['test', 'section_number']
    search_fields = ['instruction']
    list_filter = ['test']


@admin.register(ListeningQuestion)
class ListeningQuestionAdmin(admin.ModelAdmin):
    list_display = ['section', 'question_number', 'question_type', 'has_table']
    search_fields = ['question_text']
    list_filter = ['question_type', 'section__test']
    ordering = ['section', 'question_number']

    def has_table(self, obj):
        return hasattr(obj, 'table')
    has_table.boolean = True
    has_table.short_description = 'Table?'


class ListeningTableRowInline(admin.TabularInline):
    model = ListeningTableRow
    extra = 1
    fields = ['order', 'row_data']
    show_change_link = False


class ListeningTableAnswerInline(admin.TabularInline):
    model = ListeningTableAnswer
    extra = 1
    fields = ['number', 'correct_answer']
    show_change_link = False

@admin.register(ListeningTable)
class ListeningTableAdmin(admin.ModelAdmin):
    list_display = ['question']
    inlines = [ListeningTableRowInline, ListeningTableAnswerInline]
    search_fields = ['question__question_text']
@admin.register(ListeningTableRow)
class ListeningTableRowAdmin(admin.ModelAdmin):
    list_display = ['table', 'order']
    search_fields = ['row_data']
    ordering = ['table', 'order']


@admin.register(ListeningTableAnswer)
class ListeningTableAnswerAdmin(admin.ModelAdmin):
    list_display = ['table', 'number', 'correct_answer']
    search_fields = ['correct_answer']
    ordering = ['table', 'number']
