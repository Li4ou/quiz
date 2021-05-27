from main.models import Quiz, Questions, Results, Answers
from progress.models import Progress, Achievements

from rest_framework import serializers
from rest_framework.response import Response
from collections import OrderedDict


class AnswerSerializerd(serializers.ModelSerializer):
    class Meta:
        model = Answers
        fields = ['id', 'text']


class QuestionsSerializer(serializers.ModelSerializer):
    answer = AnswerSerializerd(many=True)

    class Meta:
        model = Questions
        fields = ['id', 'text', 'answer']


class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionsSerializer(read_only=True, many=True, source='questions_set')

    class Meta:
        model = Quiz
        fields = ['id', 'name', 'questions']


class QuizSerializerList(serializers.ModelSerializer):
    next = serializers.URLField(read_only=True, source='get_absolute_url')

    class Meta:
        model = Quiz
        fields = ['id', 'name', 'next', 'description','complexity']


class ResultsSerilizers(serializers.ModelSerializer):
    class Meta:
        model = Results
        fields = ['quiz', 'answer', ]


class AchievementsSerilizers(serializers.ModelSerializer):
    """Достижения"""

    class Meta:
        model = Achievements
        fields = '__all__'


class ProgressSerilizers(serializers.ModelSerializer):
    achievements = AchievementsSerilizers(many=True, read_only=True)
    class Meta:
        model = Progress
        fields = '__all__'

