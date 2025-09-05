from django.db import models

class Task(models.Model):
    STATUS_CHOICES = (("Pending", "Pending"), ("Completed", "Completed"))
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]  # ordenação padrão

    def __str__(self):
        return self.title