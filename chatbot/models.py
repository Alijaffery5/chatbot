from django.db import models
from django.contrib.auth.models import User
from django.db.models import JSONField


class Chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) # This is the user_id field
    content = JSONField(default=list)  # Use JSONField to store a list of dictionaries
    start_time = models.DateTimeField(auto_now_add=True) # Automatically set when created
    end_time = models.DateTimeField(null=True, blank=True) # Can be set when chat ends
    session_id = models.CharField(null=True, max_length=100) # Unique session id created for each chat room