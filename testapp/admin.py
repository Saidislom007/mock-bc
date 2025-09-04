from django.contrib import admin
from django.utils.html import format_html, format_html_join
from .models import (
    Mock,
    # Reading
    ReadingTest, Passage, ReadingQuestion, ReadingTable, ReadingTableRow, ReadingTableAnswer,
    # Listening
    ListeningTest, AudioSection, ListeningQuestion, ListeningTable, ListeningTableRow, ListeningTableAnswer,
    # Speaking
    SpeakingTest, SpeakingPart1Question, SpeakingPart2CueCard, SpeakingPart3Question,
    # Writing
    WritingTest, WritingTask1, WritingTask2
)

# =============================
# READING
# =============================

class ReadingTableRowInline(admin.TabularInline):
    model = ReadingTableRow
    extra = 1


class ReadingTableAnswerInline(admin.TabularInline):
    model = ReadingTableAnswer
    extra = 1

@admin.register(ReadingTable)
class ReadingTableAdmin(admin.ModelAdmin):
    list_display = ("question", "table_preview")
    autocomplete_fields = ("question",)
    inlines = [ReadingTableRowInline, ReadingTableAnswerInline]
    readonly_fields = ("table_preview",)

    def table_preview(self, obj):
        """ Jadvalni admin’da preview qilish """
        if not obj.rows.exists():
            return "⛔ Jadval hali bo‘sh"
        headers = "".join(f"<th style='border:1px solid #ccc;padding:3px;'>{col}</th>" for col in obj.columns)
        rows_html = ""
        for row in obj.rows.all():
            row_cells = "".join(f"<td style='border:1px solid #ccc;padding:3px;'>{cell}</td>" for cell in row.row_data)
            rows_html += f"<tr>{row_cells}</tr>"

        # Javoblarni ham ko‘rsatamiz
        answers = "<br>".join(f"[[{a.number}]] → <b>{a.correct_answer}</b>" for a in obj.answers.all())

        return format_html(
            "<div><table style='border:1px solid #999; border-collapse:collapse;'>"
            "<tr>{}</tr>{}</table><div style='margin-top:5px;'><b>Javoblar:</b><br>{}</div></div>",
            format_html(headers),
            format_html(rows_html),
            format_html(answers) if answers else "⛔ Javoblar kiritilmagan"
        )
    table_preview.short_description = "Preview"



@admin.register(ReadingQuestion)
class ReadingQuestionAdmin(admin.ModelAdmin):
    list_display = ("passage", "question_number", "question_type", "options_preview")
    list_filter = ("question_type", "passage__test")
    search_fields = ("question_text",)
    ordering = ("passage", "question_number")
    autocomplete_fields = ("passage",)

    fieldsets = (
        ("Asosiy ma’lumotlar", {
            "fields": ("passage", "question_number", "question_type", "instruction", "question_text")
        }),
        ("Variantlar va Javob", {
            "fields": ("options", "correct_answer")
        }),
        ("Qo‘shimcha", {
            "fields": ("diagram_labels", "paragraph_mapping"),
            "classes": ("collapse",)
        }),
    )
    radio_fields = {"question_type": admin.VERTICAL}

    def options_preview(self, obj):
        """Options ni jadval ko‘rinishida chiqaradi"""
        if not obj.options:
            return "-"
        return format_html(
            "<table style='border:1px solid #ccc; border-collapse: collapse;'>"
            "{}"
            "</table>",
            format_html_join(
                "",
                "<tr><td style='border:1px solid #ccc; padding:3px;'>{}</td></tr>",
                ((opt,) for opt in obj.options)
            )
        )
    options_preview.short_description = "Options"


@admin.register(Passage)
class PassageAdmin(admin.ModelAdmin):
    list_display = ("title", "test", "order")
    ordering = ("test", "order")
    autocomplete_fields = ("test",)
    search_fields = ("title",)


@admin.register(ReadingTest)
class ReadingTestAdmin(admin.ModelAdmin):
    list_display = ("title", "duration_minutes", "created_at")
    ordering = ("-created_at",)
    search_fields = ("title",)


# =============================
# LISTENING
# =============================

class ListeningTableRowInline(admin.TabularInline):
    model = ListeningTableRow
    extra = 1


class ListeningTableAnswerInline(admin.TabularInline):
    model = ListeningTableAnswer
    extra = 1

@admin.register(ListeningTable)
class ListeningTableAdmin(admin.ModelAdmin):
    list_display = ("question", "table_preview")
    autocomplete_fields = ("question",)
    inlines = [ListeningTableRowInline, ListeningTableAnswerInline]
    readonly_fields = ("table_preview",)

    def table_preview(self, obj):
        if not obj.rows.exists():
            return "⛔ Jadval hali bo‘sh"
        headers = "".join(f"<th style='border:1px solid #ccc;padding:3px;'>{col}</th>" for col in obj.columns)
        rows_html = ""
        for row in obj.rows.all():
            row_cells = "".join(f"<td style='border:1px solid #ccc;padding:3px;'>{cell}</td>" for cell in row.row_data)
            rows_html += f"<tr>{row_cells}</tr>"

        answers = "<br>".join(f"[[{a.number}]] → <b>{a.correct_answer}</b>" for a in obj.answers.all())

        return format_html(
            "<div><table style='border:1px solid #999; border-collapse:collapse;'>"
            "<tr>{}</tr>{}</table><div style='margin-top:5px;'><b>Javoblar:</b><br>{}</div></div>",
            format_html(headers),
            format_html(rows_html),
            format_html(answers) if answers else "⛔ Javoblar kiritilmagan"
        )
    table_preview.short_description = "Preview"

@admin.register(ListeningQuestion)
class ListeningQuestionAdmin(admin.ModelAdmin):
    list_display = ("section", "question_number", "question_type", "options_preview")
    list_filter = ("question_type", "section__test")
    search_fields = ("question_text",)
    ordering = ("section", "question_number")
    autocomplete_fields = ("section",)

    fieldsets = (
        ("Asosiy ma’lumotlar", {
            "fields": ("section", "question_number", "question_type", "instruction", "question_text")
        }),
        ("Variantlar va Javob", {
            "fields": ("options", "correct_answer")
        }),
        ("Qo‘shimcha", {
            "fields": ("map_image",),
            "classes": ("collapse",)
        }),
    )
    radio_fields = {"question_type": admin.VERTICAL}

    def options_preview(self, obj):
        """Options ni jadval ko‘rinishida chiqaradi"""
        if not obj.options:
            return "-"
        return format_html(
            "<table style='border:1px solid #ccc; border-collapse: collapse;'>"
            "{}"
            "</table>",
            format_html_join(
                "",
                "<tr><td style='border:1px solid #ccc; padding:3px;'>{}</td></tr>",
                ((opt,) for opt in obj.options)
            )
        )
    options_preview.short_description = "Options"


@admin.register(AudioSection)
class AudioSectionAdmin(admin.ModelAdmin):
    list_display = ("test", "section_number", "start_time", "end_time")
    ordering = ("test", "section_number")
    autocomplete_fields = ("test",)
    search_fields = ("test__title",)


@admin.register(ListeningTest)
class ListeningTestAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at")
    ordering = ("-created_at",)
    search_fields = ("title",)


# =============================
# SPEAKING
# =============================

@admin.register(SpeakingTest)
class SpeakingTestAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at")
    search_fields = ("title",)


@admin.register(SpeakingPart1Question)
class SpeakingPart1QuestionAdmin(admin.ModelAdmin):
    list_display = ("test", "short_question")
    search_fields = ("question_text",)
    autocomplete_fields = ("test",)

    def short_question(self, obj):
        return obj.question_text[:50] + "..." if len(obj.question_text) > 50 else obj.question_text


@admin.register(SpeakingPart2CueCard)
class SpeakingPart2CueCardAdmin(admin.ModelAdmin):
    list_display = ("test", "topic")
    search_fields = ("topic", "description")
    autocomplete_fields = ("test",)


@admin.register(SpeakingPart3Question)
class SpeakingPart3QuestionAdmin(admin.ModelAdmin):
    list_display = ("test", "short_question")
    search_fields = ("question_text",)
    autocomplete_fields = ("test",)

    def short_question(self, obj):
        return obj.question_text[:50] + "..." if len(obj.question_text) > 50 else obj.question_text


# =============================
# WRITING
# =============================

@admin.register(WritingTest)
class WritingTestAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at")
    search_fields = ("title",)


@admin.register(WritingTask1)
class WritingTask1Admin(admin.ModelAdmin):
    list_display = ("test", "short_question")
    autocomplete_fields = ("test",)

    def short_question(self, obj):
        return obj.question_text[:50] + "..." if len(obj.question_text) > 50 else obj.question_text


@admin.register(WritingTask2)
class WritingTask2Admin(admin.ModelAdmin):
    list_display = ("test", "short_question")
    autocomplete_fields = ("test",)

    def short_question(self, obj):
        return obj.question_text[:50] + "..." if len(obj.question_text) > 50 else obj.question_text


# =============================
# MOCK TEST
# =============================

@admin.register(Mock)
class MockAdmin(admin.ModelAdmin):
    list_display = ("title", "number", "status", "exam_date", "is_open_today", "created_at")
    list_filter = ("status", "exam_date")
    search_fields = ("title",)
    ordering = ("-created_at",)
    filter_horizontal = ("reading_tests", "listening_tests", "speaking_tests", "writing_tests")

    fieldsets = (
        ("Asosiy ma’lumotlar", {
            "fields": ("title", "number", "status", "description", "duration_minutes")
        }),
        ("Imtihon sanasi", {
            "fields": ("exam_date",)
        }),
        ("Testlar", {
            "fields": ("reading_tests", "listening_tests", "speaking_tests", "writing_tests")
        }),
    )
