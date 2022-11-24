from django.db import models

# Create your models here.

class Challenge(models.Model):
    name=models.CharField(max_length=200,  null=False, blank=False)
    day_created=models.DateTimeField(auto_now_add=True)
    date_start=models.DateTimeField()
    date_end=models.DateTimeField()
    description=models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

