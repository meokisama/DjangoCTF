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

class Quizz(models.Model):
    challenge_id=models.IntegerField()
    name=models.CharField(max_length=200,  null=True, blank=True)
    question=models.TextField(null=False, blank=False)
    answer=models.TextField(null=False, blank=False)
    point=models.IntegerField()

    def __str__(self):
        return self.name
    
class Hint(models.Model):
    quizz_id=models.CharField(max_length=10,  null=True, blank=True)
    content=models.TextField(null=False, blank=False)
    point=models.IntegerField()

    def __str__(self):
        return self.content
