from django.db import models
from wagtail.snippets.models import register_snippet

class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255, default="Unknown") # added default value

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Subscriber"
        verbose_name_plural = "Subscribers"

register_snippet(Subscriber)