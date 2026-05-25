from django.db import models


class AdminActionLog(models.Model):
    username = models.CharField(max_length=100)
    action = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username} - {self.action[:50]} - {self.timestamp}"
