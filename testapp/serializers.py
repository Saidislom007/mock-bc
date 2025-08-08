from rest_framework import serializers
from .models import *

# Reading
class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'

class PassageSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Passage
        fields = '__all__'

class ReadingTestSerializer(serializers.ModelSerializer):
    passages = PassageSerializer(many=True, read_only=True)

    class Meta:
        model = ReadingTest
        fields = '__all__'


# Speaking
class SpeakingPart1QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpeakingPart1Question
        fields = '__all__'

class SpeakingPart2CueCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpeakingPart2CueCard
        fields = '__all__'

class SpeakingPart3QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpeakingPart3Question
        fields = '__all__'

class SpeakingTestSerializer(serializers.ModelSerializer):
    part1_questions = SpeakingPart1QuestionSerializer(many=True, read_only=True)
    part2_cue_card = SpeakingPart2CueCardSerializer(many=True, read_only=True)
    part3_questions = SpeakingPart3QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = SpeakingTest
        fields = '__all__'


# Writing
class WritingTask1Serializer(serializers.ModelSerializer):
    class Meta:
        model = WritingTask1
        fields = '__all__'

class WritingTask2Serializer(serializers.ModelSerializer):
    class Meta:
        model = WritingTask2
        fields = '__all__'

class WritingTestSerializer(serializers.ModelSerializer):
    task1 = WritingTask1Serializer(many=True, read_only=True)
    task2 = WritingTask2Serializer(many=True, read_only=True)

    class Meta:
        model = WritingTest
        fields = '__all__'

# Listening - Table Answer
class ListeningTableAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListeningTableAnswer
        fields = ['id', 'number', 'correct_answer']


# Listening - Table Row
class ListeningTableRowSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListeningTableRow
        fields = ['id', 'order', 'row_data']


# Listening - Table
class ListeningTableSerializer(serializers.ModelSerializer):
    rows = ListeningTableRowSerializer(many=True, read_only=True)
    answers = ListeningTableAnswerSerializer(many=True, read_only=True)

    class Meta:
        model = ListeningTable
        fields = ['id', 'columns', 'rows', 'answers']

# Listening
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
            'table',  # <--- Qo‘shildi
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
class ListeningSectionSerializer(serializers.ModelSerializer):
    questions = ListeningQuestionSerializer(many=True, read_only=True)

    class Meta:
        model = AudioSection
        fields = ['id', 'section_number', 'audio_file', 'instruction', 'questions']