from unittest.util import _MAX_LENGTH
from django.db import models

# Create your models here.

class User(models.Model):
    name=models.CharField(_MAX_LENGTH=200)

    def __str__(self):
        return self.name

