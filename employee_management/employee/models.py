from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Form(models.Model):

    name = models.CharField(
        max_length=255
    )

    fields = models.JSONField()

    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )


class Employee(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    form = models.ForeignKey(
        Form,
        on_delete=models.CASCADE
    )

    data = models.JSONField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )