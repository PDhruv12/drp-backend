from datetime import time
from django.db import models

# class Event(models.Model):
#     title = models.CharField(max_length=200)
#     image = models.URLField(max_length=500)
#     description = models.TextField()
#     location = models.CharField(max_length=255)
#     host = models.CharField(max_length=100)
#     signups = models.PositiveIntegerField(default=0)
#     distance = models.FloatField(help_text="Distance in miles or kilometers")
#     date = models.DateField()
#     time = models.TimeField()
#     accepted = models.BooleanField(default=False)

#     def __str__(self):
#         return self.title

# --- User Table ---
class UserTable(models.Model):
    user_id = models.TextField(primary_key=True, editable=False, unique=True)
    name = models.TextField(null=False)
    password_hash = models.TextField(null=False)
    date_of_birth = models.DateField(null=False)
    description = models.TextField(null=False)

    def __str__(self):
        return self.name


# --- Event Table ---
class EventTable(models.Model):
    event_id = models.AutoField(primary_key=True)
    host_id = models.ForeignKey(UserTable, on_delete=models.CASCADE, related_name='host_id')
    title = models.TextField(null=False)
    description = models.TextField(null=False)
    location = models.TextField(null=False)
    start_time = models.TimeField(null=False)
    end_time = models.TimeField(null=False)
    date = models.DateField(null=False)

    def __str__(self):
        return self.title


# --- Event Image Table ---
class EventImage(models.Model):
    image_id = models.AutoField(primary_key=True)
    image = models.URLField()
    event = models.ForeignKey(EventTable, on_delete=models.CASCADE, related_name='images', unique=False)


# --- Attendees Table ---
class Attendee(models.Model):
    event = models.ForeignKey(EventTable, on_delete=models.CASCADE, unique=False)
    user = models.ForeignKey(UserTable, on_delete=models.CASCADE, unique=False)

    class Meta:
        unique_together = ('event_id', 'user_id')


# --- Bookmarks Table ---
# class Bookmark(models.Model):
#     event_id = models.ForeignKey(EventTable, on_delete=models.CASCADE, unique=False)
#     user_id = models.ForeignKey(User, on_delete=models.CASCADE, unique=False)

#     class Meta:
#         unique_together = ('event_id', 'user_id')