from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_delete
from django.dispatch import receiver
import os

# Create your models here.

class CustomUser(AbstractUser):

    tanulo = models.BooleanField(default=False)
    tanar = models.BooleanField(default=False)

    def __str__(self):
        return self.last_name + ' ' + self.first_name
    

class Territorie(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=True)
    start_date = models.IntegerField()
    end_date = models.IntegerField()
    color = models.CharField(max_length=10)
    coordinates = models.TextField(blank=False)

    def __str__(self):
        return str(self.id)+' '+self.name+str(self.start_date)+' '+str(self.end_date)

class Historie(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=True)
    description = models.TextField()
    coordinates = models.TextField(blank=True)
    HISTORIE_TYPE_CHOICHES = [
        ('csata','csata'),
        ('esemeny', 'esemény'),
    ]
    historie_type = models.CharField(max_length=255, choices=HISTORIE_TYPE_CHOICHES)
    image = models.ImageField(upload_to='historie/', default=None, blank=True)
    date = models.IntegerField(default=1000)
    

    def __str__(self):
        return str(self.id)+' '+self.name+' '+self.historie_type

@receiver(post_delete, sender=Historie)
def delete_image_file(sender, instance, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)






class CustomDraw(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=False)
    description = models.TextField(blank=True)
    coordinates = models.TextField(blank=False)
    TYPE_CHOICHES = [
        ("point","Point"),
        ("linestring", "LineString"),
        ("polygon", "Polygon"),
        
    ]
    type = models.CharField(max_length=255, blank=False, choices=TYPE_CHOICHES)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)+' '+self.name+' '+self.created_by.last_name+' '+self.created_by.first_name
    
class Quiz(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=500)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='created_quizzes', null=True, blank=True)

    def __str__(self):
        return self.title
    
class Question(models.Model):
    id = models.BigAutoField(primary_key=True)
    QUESTION_TYPES = [
        ('mc', 'Több válasz'),
        ('tf', 'Igaz/Hamis')
    ]
    quiz = models.ForeignKey(Quiz, on_delete=models.SET_NULL, related_name='questions', null=True)
    text = models.CharField(max_length=255, blank=False)
    question_type = models.CharField(max_length=2, choices=QUESTION_TYPES)
    points = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.text
class Answer(models.Model):
    id = models.BigAutoField(primary_key=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.CharField(max_length=255, blank=True)
    is_correct = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.text} ({'Correct' if self.is_correct else 'Incorrect'})"

class UserScore(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='scores')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=False)
    total_score = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.user} - {self.quiz.title}: {self.total_score} points"
class UserAnswer(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='user_answers')
    selected_answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='user_selections')
    is_correct = models.BooleanField()
    points_awarded = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.user} - {self.question.text}: {'Correct' if self.is_correct else 'Incorrect'} ({self.points_awarded} points)"