from django.db import models


class AuditLog(models.Model):
    actor = models.CharField(max_length=50)
    action = models.CharField(max_length=50)  # create/update/delete/switch-command/sync
    target_type = models.CharField(max_length=50)
    target_id = models.CharField(max_length=50, blank=True)
    detail = models.TextField(blank=True)
    acted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['acted_at']),
            models.Index(fields=['actor']),
            models.Index(fields=['target_type']),
            models.Index(fields=['action']),
        ]
        ordering = ['-acted_at']

    def __str__(self):
        return f"{self.acted_at:%Y-%m-%d %H:%M} | {self.actor} | {self.action} | {self.target_type}"
