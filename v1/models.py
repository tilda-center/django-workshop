import uuid
from django.db import models


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
