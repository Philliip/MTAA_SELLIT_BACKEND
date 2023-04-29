from django.db import models
from apps.core.models import User
from apps.core.models.base import BaseModel

class ExpoToken(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=255, unique=True)

