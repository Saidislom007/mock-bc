from django.contrib import admin
from django.utils.html import format_html
import matplotlib.pyplot as plt
import base64
from io import BytesIO

from .models import User, TestResult, OverallScore


# ================= INLINE ==================
class OverallScoreInline(admin.StackedInline):
    model = OverallScore
    can_delete = False
    verbose_name_plural = "Overall Score"
    readonly_fields = [
        'reading_band',
        'listening_band',
        'speaking_band',
        'writing_band',
        'overall_band',
        'band_chart_inline'
    ]

    def band_chart_inline(self, obj):
        """Reading/Listening/Speaking/Writing uchun mini diagramma (bar chart)"""
        if not obj:
            return "No data"

        labels = ["Reading", "Listening", "Speaking", "Writing"]
        values = [
            obj.reading_band,
            obj.listening_band,
            obj.speaking_band,
            obj.writing_band
        ]

        fig, ax = plt.subplots(figsize=(3, 2))
        ax.bar(labels, values, color=["#007bff", "#28a745", "#ffc107", "#dc3545"])
        ax.set_ylim(0, 9)
        ax.set_ylabel("Band")
        plt.tight_layout()

        buffer = BytesIO()
        plt.savefig(buffer, format="png")
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()
        plt.close(fig)  # ✅ memory leak bo‘lmasligi uchun

        chart = base64.b64encode(image_png).decode("utf-8")
        return format_html('<img src="data:image/png;base64,{}" />', chart)

    band_chart_inline.short_description = "Band Diagram"


# ================= USER ADMIN ==================
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['name', 'last_name', 'phone', 'total_tests', 'latest_score']
    search_fields = ['name', 'last_name', 'phone']
    ordering = ['last_name', 'name']

    def total_tests(self, obj):
        return obj.test_results.count()
    total_tests.short_description = "Number of Tests"

    def latest_score(self, obj):
        last_result = obj.test_results.order_by('-test_date').first()
        if not last_result or not hasattr(last_result, "overall_score"):
            return "-"
        score = last_result.overall_score.overall_band
        color = "#28a745" if score >= 6.5 else "#ffc107" if score >= 5 else "#dc3545"
        return format_html(
            '<span style="padding:4px 10px; background:{}; color:white; border-radius:5px;">{}</span>',
            color, score
        )
    latest_score.short_description = "Latest Overall Band"


# ================= TEST RESULT ADMIN ==================
@admin.register(TestResult)
class TestResultAdmin(admin.ModelAdmin):
    list_display = ['user', 'test_date', 'overall_band_preview']
    search_fields = ['user__name', 'user__last_name', 'user__phone']
    list_filter = ['test_date']
    date_hierarchy = 'test_date'
    inlines = [OverallScoreInline]
    ordering = ['-test_date']

    def overall_band_preview(self, obj):
        score = getattr(obj.overall_score, 'overall_band', None)
        if score is None:
            return "-"
        color = "#28a745" if score >= 6.5 else "#ffc107" if score >= 5 else "#dc3545"
        return format_html(
            '<span style="padding:4px 10px; background:{}; color:white; border-radius:5px;">{}</span>',
            color, score
        )
    overall_band_preview.short_description = "Overall Band"


# ================= OVERALL SCORE ADMIN ==================
@admin.register(OverallScore)
class OverallScoreAdmin(admin.ModelAdmin):
    list_display = [
        'test_result',
        'reading_band',
        'listening_band',
        'speaking_band',
        'writing_band',
        'overall_band',
        'band_preview'
    ]
    search_fields = ['test_result__user__name', 'test_result__user__last_name']
    readonly_fields = [
        'reading_band',
        'listening_band',
        'speaking_band',
        'writing_band',
        'overall_band',
        'band_chart'
    ]
    ordering = ['-overall_band']

    def band_preview(self, obj):
        """Overall band rangli badge"""
        score = obj.overall_band
        color = "#28a745" if score >= 6.5 else "#ffc107" if score >= 5 else "#dc3545"
        return format_html(
            '<span style="padding:4px 10px; background:{}; color:white; border-radius:5px;">{}</span>',
            color, score
        )
    band_preview.short_description = "Preview"

    def band_chart(self, obj):
        """Reading/Listening/Speaking/Writing uchun mini diagramma (bar chart)"""
        labels = ["Reading", "Listening", "Speaking", "Writing"]
        values = [
            obj.reading_band,
            obj.listening_band,
            obj.speaking_band,
            obj.writing_band
        ]

        fig, ax = plt.subplots(figsize=(3, 2))
        ax.bar(labels, values, color=["#007bff", "#28a745", "#ffc107", "#dc3545"])
        ax.set_ylim(0, 9)
        ax.set_ylabel("Band")
        plt.tight_layout()

        buffer = BytesIO()
        plt.savefig(buffer, format="png")
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()
        plt.close(fig)  # ✅ memory leak oldini olish

        chart = base64.b64encode(image_png).decode("utf-8")
        return format_html('<img src="data:image/png;base64,{}" />', chart)

    band_chart.short_description = "Band Diagram"
