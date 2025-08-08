from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import TestResult, OverallScore

@receiver(post_save, sender=TestResult)
def create_or_update_overall_score(sender, instance, created, **kwargs):
    if created:
        OverallScore.objects.create(test_result=instance)
    else:
        # Agar mavjud bo‘lsa — qayta hisoblaydi
        instance.overall_score.save()
