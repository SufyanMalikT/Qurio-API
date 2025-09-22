from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class CustomUser(AbstractUser):
    pass
class Tags(models.Model):
    name = models.CharField(max_length=25,unique=True)

    def __str__(self):
        return self.name

class Questions(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    author = models.ForeignKey(CustomUser, related_name="questions",on_delete=models.CASCADE)
    tags = models.ManyToManyField("Tags",blank=True,related_name='questions')
    posted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views = models.PositiveIntegerField(default=0)
    is_resolved = models.BooleanField(default=False)

    class Meta:
        ordering = ['-posted_at']
    def __str__(self):
        return self.title

    
class Answers(models.Model):
    question = models.ForeignKey(Questions,related_name="answers",on_delete=models.CASCADE)
    body = models.TextField()
    author = models.ForeignKey(CustomUser,related_name='answers',on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Vote(models.Model):
    UPVOTE = 1
    DOWNVOTE = -1
    VOTE_CHOICES = [(UPVOTE,'upvote'),(DOWNVOTE,'downvote')]

    answer = models.ForeignKey(Answers,related_name='votes',on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser,related_name='votes',on_delete=models.CASCADE)
    value = models.SmallIntegerField(choices=VOTE_CHOICES)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['user','answer'],name='unique_user_answer_vote')]


