from django.db import models
import os
import uuid
from decimal import Decimal


class User(models.Model):
    name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} {self.last_name}"



class TestResult(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='test_results')
    test_date = models.DateTimeField(auto_now_add=True)

    reading_correct_answers = models.PositiveIntegerField(default=0)
    listening_correct_answers = models.PositiveIntegerField(default=0)
    speaking_score = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)
    writing_score = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)
    def __str__(self):
        return f"{self.user.name} - Test on {self.test_date.strftime('%Y-%m-%d')}"


class OverallScore(models.Model):
    test_result = models.OneToOneField(TestResult, on_delete=models.CASCADE, related_name='overall_score')
    reading_band = models.DecimalField(max_digits=3, decimal_places=1, editable=False)
    listening_band = models.DecimalField(max_digits=3, decimal_places=1, editable=False)
    overall_band = models.DecimalField(max_digits=3, decimal_places=1, editable=False)

    @property
    def speaking_band(self):
        return self.test_result.speaking_score

    @property
    def writing_band(self):
        return self.test_result.writing_score

    def calculate_band(self, correct_answers):
        if correct_answers >= 39:
            return 9.0
        elif correct_answers >= 37:
            return 8.5
        elif correct_answers >= 35:
            return 8.0
        elif correct_answers >= 32:
            return 7.5
        elif correct_answers >= 30:
            return 7.0
        elif correct_answers >= 26:
            return 6.5
        elif correct_answers >= 23:
            return 6.0
        elif correct_answers >= 18:
            return 5.5
        elif correct_answers >= 16:
            return 5.0
        elif correct_answers >= 13:
            return 4.5
        elif correct_answers >= 10:
            return 4.0
        else:
            return 3.5

    def round_band(self, score):
        decimal = float(score) % 1
        if decimal < 0.25:
            return float(round(score))
        elif decimal < 0.75:
            return float(round(score * 2) / 2)
        else:
            return float(round(score))

    def save(self, *args, **kwargs):
        self.reading_band = self.calculate_band(self.test_result.reading_correct_answers)
        self.listening_band = self.calculate_band(self.test_result.listening_correct_answers)

        raw_average = (
            Decimal(self.reading_band) + Decimal(self.listening_band) +
            Decimal(self.speaking_band) + Decimal(self.writing_band)
        ) / Decimal(4)

        self.overall_band = self.round_band(raw_average)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.test_result.user.name} - Overall Band: {self.overall_band}"
