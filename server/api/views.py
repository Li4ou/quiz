from main.models import Quiz, Results, Answers

from api.serializers import (QuizSerializerList,
                             QuestionsSerializer, ResultsSerilizers, ProgressSerilizers
                             )
from api.paginators import CustomPagination
from progress.models import Progress, Achievements

from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response


class QuestionsView(generics.ListAPIView):
    serializer_class = QuestionsSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        return Quiz.objects.get(pk=self.kwargs['pk']).questions_set.all().prefetch_related('answer')

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_paginated_response(self, data):
        """
        Return a paginated style `Response` object for the given output data.
        """
        assert self.paginator is not None
        return self.paginator.get_paginated_response(self.kwargs['pk'], data)


class QuizViewSet(generics.ListAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializerList


class ResultsAPIView(generics.CreateAPIView):
    models = Results
    queryset = Results.objects.all()
    serializer_class = ResultsSerilizers

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        self.get_correct_answers(serializer)
        return Response(self.get_content(), status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        """ Пользователь"""
        serializer.save(user=self.request.user)

    def get_correct_answers(self, serializer):
        answers = Answers.objects.filter(id__in=serializer['answer'].value)
        self.correct = 0
        self.count = len(answers)
        for item in answers:
            self.correct += 1 if item.correct else 0
        if self.correct == len(answers): self.add_quiz_achievement(serializer)
        if self.correct == 0: self.add_achievement_dunno(serializer)

    def add_achievement_dunno(self, serializer):
        achievements_id = 3  # id достижения незнайка
        achievements = Achievements.objects.get(id=achievements_id)
        progress = Progress.objects.get(id=self.request.user.id)
        progress.achievements.add(achievements)
        progress.save()

    def add_quiz_achievement(self, serializer):
        quiz = Quiz.objects.get(id=serializer['quiz'].value)
        progress = Progress.objects.get(id=self.request.user.id)
        progress.achievements.add(quiz.achievements)
        progress.save()

    def get_content(self):
        return {
            'correct': self.correct,
            'count': self.count,
        }


class NagradyAPIView(generics.ListAPIView):
    """Список наград"""
    serializer_class = ProgressSerilizers

    def get_queryset(self):
        return self.request.user.progress_set.all()
