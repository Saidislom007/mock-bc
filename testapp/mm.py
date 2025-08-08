# from django.db import models
# import uuid
# from django.core.validators import MinValueValidator, MaxValueValidator

# class Mock(models.Model):
#     """
#     Har bir IELTS test sessiyasi (Mock Test ID)
#     """
#     title = models.CharField(max_length=255)
#     description = models.TextField(blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.title
    



# class ReadingPassage1(models.Model):
#     title = models.CharField(max_length=255)
#     passage_text = models.TextField()

#     def __str__(self):
#         return self.title


# class ReadingPassage1TFQuestion(models.Model):
#     instruction = models.TextField(help_text="Ko'rsatma matni")
#     passage = models.ForeignKey(ReadingPassage1, related_name='tf_questions', on_delete=models.CASCADE)
#     question_number = models.PositiveIntegerField(
#         validators=[
#             MinValueValidator(1),
#             MaxValueValidator(6)
#         ],
#         help_text="Faqat 1 dan 6 gacha bo'lgan savol raqamlari kiritiladi"
#     )
#     question_text = models.TextField()

#     correct_answer = models.CharField(
#         max_length=10,
#         choices=[
#             ('TRUE', 'TRUE'),
#             ('FALSE', 'FALSE'),
#             ('NOT GIVEN', 'NOT GIVEN'),
#         ],
#         help_text="To‘g‘ri javob"
#     )

#     def __str__(self):
#         return f"Q{self.question_number}: {self.correct_answer}"

# class ReadingPassage1CompletionQuestion(models.Model):
#     instruction = models.TextField(help_text="Ko'rsatma matni uchun ",default='')
#     passage = models.ForeignKey(ReadingPassage1, related_name='completion_questions', on_delete=models.CASCADE)
#     question_number = models.PositiveIntegerField(
#         validators=[
#             MinValueValidator(7),
#             MaxValueValidator(13)
#         ],
#         help_text="Faqat 7 dan 13 gacha bo'lgan savol raqamlari kiritiladi"
#     )
#     prompt_text = models.TextField(help_text="Savol yoki gap: blank joy bilan")
#     correct_answer = models.CharField(max_length=255, help_text="To‘g‘ri javob (ONE WORD / NUMBER)")

#     def __str__(self):
#         return f"Q{self.question_number}: {self.correct_answer}"



# class ReadingPassage2Options(models.Model):
#     option_title = models.CharField(max_length=1,default="A")
#     body = models.TextField(default='')


# class ReadingPassage2(models.Model):
#     title = models.CharField(max_length=255)
#     passage_body = models.ForeignKey(ReadingPassage2Options,related_name='reading_passage_2_options', on_delete=models.CASCADE)
#     def __str__(self):
#         return self.title
    


# class ReadingPassage2MCHQuestion(models.Model):
#     instruction = models.TextField(help_text="Ko'rsatma matni")
#     passage = models.ForeignKey(ReadingPassage2, related_name='mch_questions', on_delete=models.CASCADE)
#     question_number = models.PositiveIntegerField(
#         validators=[
#             MinValueValidator(14),
#             MaxValueValidator(18)
#         ],
#         help_text="Faqat 14 dan 18 gacha bo'lgan savol raqamlari kiritiladi"
#     )
#     question_text = models.TextField()
#     correct_answer = models.CharField(
#         max_length=1,
#         choices=[
#             ('A', 'A'),
#             ('B', 'B'),
#             ('C ', 'C'),
#             ('D', 'D'),
#             ('E', 'E'),
#             ('F', 'F'),
#             ('H', 'H'),
#         ],
#         help_text="To'gri javob"
#     )
    
#     def __str__(self):
#         return f"Q{self.question_number}: {self.correct_answer}"

# class ReadingPassage2MCH2Questions(models.Model):
#     instruction = models.TextField(help_text="Ko'rsatma matni",default='')
#     passage = models.ForeignKey(ReadingPassage2, related_name='mch2_questions', on_delete=models.CASCADE)
#     question_number = models.PositiveIntegerField(
#         validators=[
#             MinValueValidator(19),
#             MaxValueValidator(23)
#         ],
#         help_text="Faqat 19 dan 23 gacha bo'lgan savol raqamlari kiritiladi"
#     )
#     question_text = models.TextField()
#     correct_answer = models.CharField(
#         max_length=1,
#         choices=[
#             ('A', 'A'),
#             ('B', 'B'),
#             ('C ', 'C'),
#         ],
#         help_text="To'gri javob"
#     )
    
#     def __str__(self):
#         return f"Q{self.question_number}: {self.correct_answer}"

# class ReadingPassage2CompletionQuestions(models.Model):
#     instruction = models.TextField(help_text="Ko'rsatma matni",default='')
#     passage = models.ForeignKey(ReadingPassage2, related_name='comp_questions', on_delete=models.CASCADE)
#     question_number = models.PositiveIntegerField(
#         validators=[
#             MinValueValidator(24),
#             MaxValueValidator(26)
#         ],
#         help_text="Faqat 24 dan 26 gacha bo'lgan savol raqamlari kiritiladi"
#     )
#     question_text = models.TextField()
#     correct_answer = models.CharField(
#         max_length=1,
#         choices=[
#             ('A', 'A'),
#             ('B', 'B'),
#             ('C ', 'C'),
#         ],
#         help_text="To'gri javob"
#     )
    
#     def __str__(self):
#         return f"Q{self.question_number}: {self.correct_answer}"


















# class ReadingMock(models.Model):
#     mock = models.ForeignKey(Mock, related_name='reading_mock', on_delete=models.CASCADE)
#     passage_1 = models.ForeignKey(ReadingPassage1,related_name='passage_1',on_delete=models.CASCADE)

#     def __str__(self):
#         return str(self.mock)  





