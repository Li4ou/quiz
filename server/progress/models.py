from django.db import models
from django.contrib.auth.models import User
from django.db.models import signals
from django.dispatch import receiver


class Progress(models.Model):
    """Прогресс"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    balls = models.IntegerField("Баллы", default=0)
    achievements = models.ManyToManyField("Achievements")

    class Meta:
        verbose_name = "Прогрес"
        verbose_name_plural = "Прогрес"


class Achievements(models.Model):
    """Достижения"""
    TYPE = (
        ("Commmon", "Commmon"),
        ("Uncommon", "Uncommon"),
        ("Rare", "Rare"),
        ("Legendary", "Legendary"),

    )
    title = models.CharField("Заголовок", max_length=255)
    type = models.CharField(max_length=255, choices=TYPE)
    lvl = models.IntegerField("Lvl")
    balls = models.IntegerField("Балы")
    description = models.TextField("Описание", blank=True)
    image = models.ImageField("Значок")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Достижение"
        verbose_name_plural = "Достижения"


@receiver(signals.post_save, sender=User)
def create_customer(sender, instance, created, **kwargs):
    """Создание экзампляра модела  Progress  при регистрации пользователя """
    achievements_id = 2  # id достижения Австоризованный полльзователь
    progress = Progress()
    progress.user = instance
    progress.balls = 0
    progress.save()
    progress.achievements.add(Achievements.objects.get(id=achievements_id))
    progress.save()
