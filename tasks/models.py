from django.db import models
from django.conf import settings

class Task(models.Model):
    STATUS_CHOICES = (("Pending", "Pending"), ("Completed", "Completed"))
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="tasks",
    )

    class Meta:
        ordering = ["-created_at"]  # default ordenation

    def __str__(self):
        return self.title # see title of task