from django.db import models
from django.contrib.auth.models import User

class Todo(models.Model):
    text = models.CharField(max_length=200)
    description = models.CharField(max_length=1000, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.pk}: {self.text}, {self.description}'
