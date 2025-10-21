# feelingss/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    bio = models.TextField(max_length=500, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.username


class Feeling(models.Model):
    EMOTION_CHOICES = [
        ('happy', '😊 Счастлив'),
        ('sad', '😢 Грустный'),
        ('angry', '😠 Злой'),
        ('excited', '🤩 Взволнованный'),
        ('calm', '😌 Спокойный'),
        ('anxious', '😰 Тревожный'),
        ('grateful', '🙏 Благодарный'),
        ('tired', '😴 Уставший'),
    ]

    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    text = models.TextField(verbose_name='Текст чувства')
    emotion = models.CharField(
        max_length=20,
        choices=EMOTION_CHOICES,
        verbose_name='Эмоция'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']  # Теперь поле существует

    def __str__(self):
        return f"{self.user.username}: {self.emotion}"