from django.db import models
from auth_app.models import CustomUser

class DriverMatch(models.Model):
    driver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='driver_matches')
    criteria = models.TextField()  # Criteria for matching
    matched_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Match for {self.driver.username} at {self.matched_at}"
