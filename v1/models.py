import uuid
from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class VerifyToken(models.Model):
    token = models.UUIDField(
            primary_key=True,
            default=uuid.uuid4,
            editable=False
    )
    email = models.EmailField(unique=True)
    used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)


class Event(models.Model):
    start = models.DateTimeField()
    end = models.DateTimeField()
    info = models.TextField(max_length=500)


class Lecture(models.Model):
    professor = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
    )
    students = models.ManyToManyField(User, related_name="Class")
    events = models.ManyToManyField(Event)
    title = models.TextField(max_length=100)
    info = models.TextField(max_length=500)
