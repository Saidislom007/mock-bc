from django.contrib import admin
from .models import User, TestResult, OverallScore

# OverallScore ni TestResult sahifasida inline ko‘rsatish
class OverallScoreInline(admin.StackedInline):
    model = OverallScore
    can_delete = False
    verbose_name_plural = "Overall Score"
    readonly_fields = ['reading_band', 'listening_band', 'speaking_band', 'writing_band', 'overall_band']
    # Property metodlar uchun admin panelda ko‘rsatish
    def speaking_band(self, obj):
        return obj.speaking_band
    speaking_band.short_description = "Speaking Band"
    
    def writing_band(self, obj):
        return obj.writing_band
    writing_band.short_description = "Writing Band"


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['name', 'last_name', 'phone']
    search_fields = ['name', 'last_name', 'phone']


@admin.register(TestResult)
class TestResultAdmin(admin.ModelAdmin):
    list_display = ['user', 'test_date']
    search_fields = ['user__name', 'user__last_name', 'user__phone']
    list_filter = ['test_date']
    date_hierarchy = 'test_date'
    inlines = [OverallScoreInline]


@admin.register(OverallScore)
class OverallScoreAdmin(admin.ModelAdmin):
    list_display = ['test_result', 'overall_band']
    search_fields = ['test_result__user__name', 'test_result__user__last_name']
    readonly_fields = ['reading_band', 'listening_band', 'speaking_band', 'writing_band', 'overall_band']

    def speaking_band(self, obj):
        return obj.speaking_band
    speaking_band.short_description = "Speaking Band"

    def writing_band(self, obj):
        return obj.writing_band
    writing_band.short_description = "Writing Band"
