from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone


# =========================================
# MOCK TEST MODEL
# =========================================
class Mock(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("active", "Active"),
        ("inactive", "Inactive"),
    ]

    title = models.CharField(max_length=255)
    number = models.PositiveIntegerField(unique=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )
    description = models.TextField(blank=True, null=True)
    duration_minutes = models.PositiveIntegerField(default=120)
    exam_date = models.DateField(help_text="Imtihon sanasi. Faqat shu kunda aktiv bo‘ladi.")
    created_at = models.DateTimeField(auto_now_add=True)

    reading_tests = models.ManyToManyField('ReadingTest', blank=True, related_name='mocks')
    listening_tests = models.ManyToManyField('ListeningTest', blank=True, related_name='mocks')
    speaking_tests = models.ManyToManyField('SpeakingTest', blank=True, related_name='mocks')
    writing_tests = models.ManyToManyField('WritingTest', blank=True, related_name='mocks')

    class Meta:
        ordering = ['-created_at']

    def clean(self):
        """Faqat bitta mock active bo‘lishiga ruxsat beramiz"""
        if self.status == "active":
            active_mocks = Mock.objects.filter(status="active").exclude(id=self.id)
            if active_mocks.exists():
                raise ValidationError("Faqat bitta Mock test active bo‘lishi mumkin!")

        if self.exam_date < timezone.now().date():
            raise ValidationError("Imtihon sanasi o'tmishda bo‘lishi mumkin emas!")

    def is_open_today(self):
        """Bugungi kunda test ochiqmi?"""
        return self.status == "active" and self.exam_date == timezone.now().date()

    def save(self, *args, **kwargs):
        self.full_clean()  # validatsiya ishlaydi
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({self.get_status_display()} | {self.exam_date})"


# =========================================
# READING TEST MODELS
# =========================================
class ReadingTest(models.Model):
    title = models.CharField(max_length=255)
    duration_minutes = models.PositiveIntegerField(default=60)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Passage(models.Model):
    test = models.ForeignKey(
        ReadingTest,
        on_delete=models.CASCADE,
        related_name='passages'
    )
    instruction = models.TextField(default='')
    title = models.CharField(max_length=255)
    text = models.TextField()
    order = models.PositiveIntegerField(
        help_text="Passage 1, 2, 3 uchun tartib raqami"
    )

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.test.title} - Passage {self.order}"


class ReadingQuestion(models.Model):
    QUESTION_TYPES = [
        ('multiple_choice', 'Multiple Choice'),
        ('true_false_not_given', 'True/False/Not Given'),
        ('matching_headings', 'Matching Headings'),
        ('sentence_completion', 'Sentence Completion'),
        ('diagram_labeling', 'Diagram Labeling'),
        ('table_completion', 'Table Completion'),
        ('two_multiple_choice', 'Two Multiple Choice'),
    ]

    instruction = models.TextField(blank=True, null=True)
    passage = models.ForeignKey(
        Passage,
        on_delete=models.CASCADE,
        related_name='questions'
    )
    question_type = models.CharField(max_length=50, choices=QUESTION_TYPES)
    question_text = models.TextField(blank=True, null=True)
    question_number = models.PositiveIntegerField(
        help_text="Question number in the test"
    )

    options = models.JSONField(blank=True, null=True)
    diagram_labels = models.ImageField(
        upload_to='reading/diagram_labels/',
        blank=True,
        null=True
    )
    paragraph_mapping = models.JSONField(blank=True, null=True)

    correct_answer = models.JSONField(
        help_text="Correct answer(s), format depends on question type"
    )

    linked_question = models.OneToOneField(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="parent_question",
        help_text="Two Multiple Choice uchun bog‘langan savol"
    )

    class Meta:
        ordering = ['question_number']

    def save(self, *args, **kwargs):
        creating = self._state.adding  # yangi yaratilayotganini tekshiramiz
        super().save(*args, **kwargs)

        # Agar yangi two_multiple_choice bo'lsa - ikkinchi savol yaratamiz
        if creating and self.question_type == "two_multiple_choice" and not self.linked_question:
            second_question = ReadingQuestion.objects.create(
                instruction=self.instruction,
                passage=self.passage,
                question_type="two_multiple_choice",
                question_text=f"{self.question_text}",
                question_number=self.question_number + 1,
                options=self.options,
                correct_answer=self.correct_answer,
            )
            self.linked_question = second_question
            super().save(update_fields=["linked_question"])

    def __str__(self):
        return f"{self.passage.title} - Q{self.question_number}: {self.question_type}"

class ReadingTable(models.Model):
    question = models.OneToOneField(
        ReadingQuestion,
        on_delete=models.CASCADE,
        related_name="table"
    )
    columns = models.JSONField(
        help_text="List of column headers"
    )

    def __str__(self):
        return f"Table for {self.question}"


class ReadingTableRow(models.Model):
    table = models.ForeignKey(
        ReadingTable,
        on_delete=models.CASCADE,
        related_name="rows"
    )
    row_data = models.JSONField(
        help_text="List of row items, include [[n]] where needed"
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        preview = ", ".join(self.row_data)[:40]
        return f"Row {self.order}: {preview}"


class ReadingTableAnswer(models.Model):
    table = models.ForeignKey(
        ReadingTable,
        on_delete=models.CASCADE,
        related_name="answers"
    )
    number = models.PositiveIntegerField(
        help_text="The number inside [[n]]"
    )
    correct_answer = models.CharField(max_length=255)

    class Meta:
        unique_together = ('table', 'number')

    def __str__(self):
        return f"Answer [[{self.number}]] = {self.correct_answer}"


# =========================================
# SPEAKING TEST MODELS
# =========================================
class SpeakingTest(models.Model):
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Speaking Test: {self.title}"


class BaseQuestion(models.Model):
    test = models.ForeignKey(
        SpeakingTest,
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=255, blank=True, default='')
    question_text = models.TextField()

    class Meta:
        abstract = True


class SpeakingPart1Question(BaseQuestion):
    class Meta:
        verbose_name = "Speaking Part 1 Question"
        verbose_name_plural = "Speaking Part 1 Questions"

    def __str__(self):
        return f"Part 1 - {self.question_text[:50]}"


class SpeakingPart2CueCard(models.Model):
    test = models.OneToOneField(
        SpeakingTest,
        on_delete=models.CASCADE,
        related_name='part2_cue_card'
    )
    topic = models.CharField(max_length=255)
    description = models.TextField(
        help_text="Full cue card prompt with bullet points"
    )

    def __str__(self):
        return f"Part 2 - {self.topic}"


class SpeakingPart3Question(BaseQuestion):
    class Meta:
        verbose_name = "Speaking Part 3 Question"
        verbose_name_plural = "Speaking Part 3 Questions"

    def __str__(self):
        return f"Part 3 - {self.question_text[:50]}"


# =========================================
# WRITING TEST MODELS
# =========================================
class WritingTest(models.Model):
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class WritingTask1(models.Model):
    test = models.ForeignKey(
        WritingTest,
        on_delete=models.CASCADE,
        related_name='task1'
    )
    question_text = models.TextField(
        help_text="Task 1 question (e.g. graph/letter description)"
    )
    image = models.ImageField(
        upload_to='writing/task1/',
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.test.title} - Task 1"


class WritingTask2(models.Model):
    test = models.ForeignKey(
        WritingTest,
        on_delete=models.CASCADE,
        related_name='task2'
    )
    question_text = models.TextField(
        help_text="Task 2 essay prompt"
    )

    def __str__(self):
        return f"{self.test.title} - Task 2"


# =========================================
# LISTENING TEST MODELS
# =========================================
class ListeningTest(models.Model):
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class AudioSection(models.Model):
    test = models.ForeignKey(
        ListeningTest,
        on_delete=models.CASCADE,
        related_name='sections'
    )
    section_number = models.PositiveIntegerField(
        help_text="Section 1, 2, 3, or 4"
    )
    instruction = models.TextField(blank=True, null=True)
    start_time = models.DurationField(
        blank=True, null=True,
        help_text="Optional: start time in audio"
    )
    end_time = models.DurationField(
        blank=True, null=True,
        help_text="Optional: end time in audio"
    )
    audio_file = models.FileField(
        upload_to='listening/sections/',
        blank=True,
        null=True
    )

    class Meta:
        ordering = ['section_number']

    def __str__(self):
        return f"{self.test.title} - Section {self.section_number}"


class ListeningQuestion(models.Model):
    QUESTION_TYPES = [
        ('multiple_choice', 'Multiple Choice'),
        ('table_completion', 'Table Completion'),
        ('map_labelling', 'Map Labelling'),
        ('sentence_completion', 'Sentence Completion'),
        ('two_multiple_choice', 'Two Multiple Choice'),
        ('true_false_not_given', 'True/False/Not Given'),
        ('matching_headings', 'Matching Headings'),
    ]

    section = models.ForeignKey(
        AudioSection,
        on_delete=models.CASCADE,
        related_name='questions'
    )
    question_number = models.PositiveIntegerField()
    question_type = models.CharField(max_length=50, choices=QUESTION_TYPES)
    question_text = models.TextField(blank=True, null=True)
    options = models.JSONField(blank=True, null=True)
    correct_answer = models.JSONField(
        help_text="Correct answer(s), format depends on question type"
    )
    instruction = models.TextField(blank=True, null=True)
    map_image = models.ImageField(
        upload_to='listening/maps/',
        blank=True,
        null=True,
        help_text="Only used for map labelling questions"
    )

    class Meta:
        ordering = ['question_number']
        unique_together = ('section', 'question_number')
    def save(self, *args, **kwargs):
        creating = self._state.adding  # yangi yaratilayotganini tekshiramiz
        super().save(*args, **kwargs)

        # Agar yangi two_multiple_choice bo'lsa - ikkinchi savol yaratamiz
        if creating and self.question_type == "two_multiple_choice" and not self.linked_question:
            second_question = ListeningQuestion.objects.create(
                instruction=self.instruction,
                passage=self.section,
                question_type="two_multiple_choice",
                question_text=f"{self.question_text}",
                question_number=self.question_number + 1,
                options=self.options,
                correct_answer=self.correct_answer,
            )
            self.linked_question = second_question
            super().save(update_fields=["linked_question"])
    def __str__(self):
        return f"{self.section} - Q{self.question_number}"


class ListeningTable(models.Model):
    question = models.OneToOneField(
        ListeningQuestion,
        on_delete=models.CASCADE,
        related_name="table"
    )
    columns = models.JSONField(
        help_text="List of column headers"
    )

    def __str__(self):
        return f"Table for {self.question}"


class ListeningTableRow(models.Model):
    table = models.ForeignKey(
        ListeningTable,
        on_delete=models.CASCADE,
        related_name="rows"
    )
    row_data = models.JSONField(
        help_text="List of row items, include [[n]] where needed"
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        preview = ", ".join(self.row_data)[:40]
        return f"Row {self.order}: {preview}"


class ListeningTableAnswer(models.Model):
    table = models.ForeignKey(
        ListeningTable,
        on_delete=models.CASCADE,
        related_name="answers"
    )
    number = models.PositiveIntegerField(
        help_text="The number inside [[n]]"
    )
    correct_answer = models.CharField(max_length=255)

    class Meta:
        unique_together = ('table', 'number')

    def __str__(self):
        return f"Answer [[{self.number}]] = {self.correct_answer}"
