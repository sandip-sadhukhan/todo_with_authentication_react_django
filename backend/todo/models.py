from django.db import models
from accounts.models import User


class Todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.CharField(max_length=255, null=False, blank=False)

    def __str__(self):
        return str(self.body)
