from rest_framework import serializers
from .models import *


# =========================================
# MOCK
# =========================================
class MockSerializer(serializers.ModelSerializer):
    reading_tests = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    listening_tests = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    speaking_tests = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    writing_tests = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Mock
        fields = '__all__'


# =========================================
# READING
# =========================================
class ReadingQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReadingQuestion
        fields = '__all__'


class PassageSerializer(serializers.ModelSerializer):
    questions = ReadingQuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Passage
        fields = '__all__'


class ReadingTestSerializer(serializers.ModelSerializer):
    passages = PassageSerializer(many=True, read_only=True)

    class Meta:
        model = ReadingTest
        fields = '__all__'


# =========================================
# SPEAKING
# =========================================
class SpeakingPart1QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpeakingPart1Question
        fields = ["id", "question_text"]


class SpeakingPart1Serializer(serializers.ModelSerializer):
    questions = SpeakingPart1QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = SpeakingPart1
        fields = ["id", "topic", "questions"]


# Part 2
class SpeakingPart2CueCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpeakingPart2CueCard
        fields = ["id", "topic", "description"]


# Part 3
class SpeakingPart3QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpeakingPart3Question
        fields = ["id", "question_text"]


class SpeakingPart3Serializer(serializers.ModelSerializer):
    questions = SpeakingPart3QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = SpeakingPart3
        fields = ["id", "topic", "questions"]


# Test
class SpeakingTestSerializer(serializers.ModelSerializer):
    part1 = SpeakingPart1Serializer(read_only=True)
    part2 = SpeakingPart2CueCardSerializer(read_only=True)
    part3 = SpeakingPart3Serializer(read_only=True)

    class Meta:
        model = SpeakingTest
        fields = ["id", "title", "created_at", "part1", "part2", "part3"]


# =========================================
# WRITING
# =========================================
class WritingTask1Serializer(serializers.ModelSerializer):
    class Meta:
        model = WritingTask1
        fields = '__all__'


class WritingTask2Serializer(serializers.ModelSerializer):
    class Meta:
        model = WritingTask2
        fields = '__all__'


class WritingTestSerializer(serializers.ModelSerializer):
    # ❌ many=True emas, chunki OneToOneField
    task1 = WritingTask1Serializer(read_only=True)
    task2 = WritingTask2Serializer(read_only=True)

    class Meta:
        model = WritingTest
        fields = '__all__'


# =========================================
# LISTENING (Tables)
# =========================================
class ListeningTableAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListeningTableAnswer
        fields = ['id', 'number', 'correct_answer']


class ListeningTableRowSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListeningTableRow
        fields = ['id', 'order', 'row_data']


class ListeningTableSerializer(serializers.ModelSerializer):
    rows = ListeningTableRowSerializer(many=True, read_only=True)
    answers = ListeningTableAnswerSerializer(many=True, read_only=True)

    class Meta:
        model = ListeningTable
        fields = ['id', 'columns', 'rows', 'answers']


# =========================================
# LISTENING (Questions & Sections)
# =========================================
class ListeningQuestionSerializer(serializers.ModelSerializer):
    table = ListeningTableSerializer(read_only=True)

    class Meta:
        model = ListeningQuestion
        fields = [
            'id',
            'section',
            'question_number',
            'question_type',
            'question_text',
            'instruction',
            'options',
            'correct_answer',
            'map_image',
            'table',
        ]


class AudioSectionSerializer(serializers.ModelSerializer):
    questions = ListeningQuestionSerializer(many=True, read_only=True)

    class Meta:
        model = AudioSection
        fields = '__all__'


class ListeningTestSerializer(serializers.ModelSerializer):
    sections = AudioSectionSerializer(many=True, read_only=True)

    class Meta:
        model = ListeningTest
        fields = '__all__'


# Soddalashtirilgan variant (faqat section-level)
class ListeningSectionSerializer(serializers.ModelSerializer):
    questions = ListeningQuestionSerializer(many=True, read_only=True)

    class Meta:
        model = AudioSection
        fields = ['id', 'section_number', 'audio_file', 'instruction', 'questions']
