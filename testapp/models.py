from django.db import models


# =========================================
# MOCK TEST MODEL
# =========================================
class Mock(models.Model):
    title = models.CharField(max_length=255)
    number = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


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
        ('summary_completion', 'Summary Completion'),
        ('diagram_labeling', 'Diagram Labeling'),
        ('short_answer', 'Short Answer'),
    ]

    instruction = models.TextField(blank=True, null=True)
    passage = models.ForeignKey(
        Passage,
        on_delete=models.CASCADE,
        related_name='questions'
    )
    question_type = models.CharField(max_length=50, choices=QUESTION_TYPES)
    question_text = models.TextField()
    question_number = models.PositiveIntegerField(
        help_text="Question number in the test"
    )

    # Optional fields depending on question type
    options = models.JSONField(blank=True, null=True)
    summary_text = models.TextField(blank=True, null=True)
    diagram_labels = models.JSONField(blank=True, null=True)
    paragraph_mapping = models.JSONField(blank=True, null=True)

    correct_answer = models.JSONField(
        help_text="Correct answer(s), format depends on question type"
    )

    class Meta:
        ordering = ['question_number']

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
        return self.title


class SpeakingPart1Question(models.Model):
    test = models.ForeignKey(
        SpeakingTest,
        on_delete=models.CASCADE,
        related_name='part1_questions'
    )
    title = models.TextField(default='')
    question_text = models.TextField()

    def __str__(self):
        return f"Part 1 - {self.question_text[:50]}"


class SpeakingPart2CueCard(models.Model):
    test = models.ForeignKey(
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


class SpeakingPart3Question(models.Model):
    test = models.ForeignKey(
        SpeakingTest,
        on_delete=models.CASCADE,
        related_name='part3_questions'
    )
    title = models.TextField(default='')
    question_text = models.TextField()

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
        ('form_completion', 'Form Completion'),
        ('table_completion', 'Table Completion'),
        ('note_completion', 'Note Completion'),
        ('map_labelling', 'Map Labelling'),
        ('matching', 'Matching'),
        ('sentence_completion', 'Sentence Completion'),
        ('short_answer', 'Short Answer'),
    ]

    section = models.ForeignKey(
        AudioSection,
        on_delete=models.CASCADE,
        related_name='questions'
    )
    question_number = models.PositiveIntegerField()
    question_type = models.CharField(max_length=50, choices=QUESTION_TYPES)
    question_text = models.TextField()
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
