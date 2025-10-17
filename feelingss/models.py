from django.db import models


class Feeling(models.Model):
    name = models.CharField(max_length=50)  # Название чувства
    description = models.TextField()  # Описание чувства

    def __str__(self):
        return self.name
from django.db import models

# Create your models here.
