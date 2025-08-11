from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class BaseModel(models.Model):
    """
    Data model to save common data used in models.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Task(BaseModel):
    """
    Task model to save and manage task details
    """
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    completed = models.BooleanField(default=False)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="tasks"
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} ({'done' if self.completed else 'todo'})"
