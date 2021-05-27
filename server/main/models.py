from progress.models import Achievements, Progress
from django.db import models
from django.contrib.auth.models import User
from django.db.models import signals
from django.dispatch import receiver


class Quiz(models.Model):
    """Витторина"""
    COMPLEXITY = (
        ("1", 'easy'),
        ("2", 'medium'),
        ("3", 'hard')
    )

    name = models.CharField('Заголовок', max_length=255)
    description = models.TextField("Описание", blank=True)
    complexity = models.CharField("Сложность", max_length=10, choices=COMPLEXITY, default=1)
    achievements = models.OneToOneField(Achievements, verbose_name="Достажение", on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Викторина'
        verbose_name_plural = 'Викторины'

    def get_questions(self):
        return self.questions_set.all()

    def get_absolute_url(self):
        return f"'/api/quiz/questions/{self.id}'"


class Answers(models.Model):
    """Ответы"""
    text = models.CharField('Ответ', max_length=255)
    correct = models.BooleanField()

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"


class Questions(models.Model):
    """Вопросы"""
    text = models.CharField('Заголовок', max_length=255)
    quiz = models.ForeignKey(Quiz, verbose_name='Викторина', on_delete=models.CASCADE)
    answer = models.ManyToManyField(Answers)

    class Meta:
        ordering = ['id']
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

    def __str__(self):
        return self.text

    def get_answer(self):
        return self.answer.all()


class Results(models.Model):
    """Результаты викторины"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, )
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    answer = models.ManyToManyField(Answers)

    class Meta:
        verbose_name = "Результаты викторины"
        verbose_name_plural = "Результаты викторины"
