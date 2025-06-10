from datetime import time
import random
from django.db import models

def generate_random_distance():
    return round(random.uniform(0, 10), 1)

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
    distance = models.FloatField(default=generate_random_distance)
    price = models.FloatField(default=0.0)
    over = models.BooleanField(default=False)

    def __str__(self):
        return self.title


# --- Event Image Table ---
class EventImage(models.Model):
    image_id = models.AutoField(primary_key=True)
    image = models.TextField()
    event = models.ForeignKey(EventTable, on_delete=models.CASCADE, related_name='images', unique=False)


# --- Attendees Table ---
class Attendee(models.Model):
    event = models.ForeignKey(EventTable, on_delete=models.CASCADE, unique=False)
    user = models.ForeignKey(UserTable, on_delete=models.CASCADE, unique=False)

    class Meta:
        unique_together = ('event_id', 'user_id')

# --- Tags Table ---
class Tag(models.Model):
    event = models.ForeignKey(EventTable, on_delete=models.CASCADE, unique=False)
    tag_name = models.TextField()

class Cohost(models.Model):
    event = models.ForeignKey(EventTable, on_delete=models.CASCADE, related_name='event_cohost', unique=False)
    host = models.ForeignKey(UserTable, on_delete=models.CASCADE, related_name='co_host', unique=False)

    class Meta:
        unique_together = ('event', 'host')

# --- Community Table ---
class Community(models.Model):
    community_id = models.AutoField(primary_key=True)
    name = models.TextField()
    description = models.TextField()

class CommunityTag(models.Model):
    community = models.ForeignKey(Community, on_delete=models.CASCADE, unique=False)
    tag_name = models.TextField()

class CommunityImage(models.Model):
    image_id = models.AutoField(primary_key=True)
    image = models.TextField()
    community = models.ForeignKey(Community, on_delete=models.CASCADE, unique=False)

class CommunityMember(models.Model):
    community = models.ForeignKey(Community, on_delete=models.CASCADE, unique=False)
    user = models.ForeignKey(UserTable, on_delete=models.CASCADE, unique=False)

    class Meta:
        unique_together = ('community', 'user')

# --- Bookmarks Table ---
# class Bookmark(models.Model):
#     event_id = models.ForeignKey(EventTable, on_delete=models.CASCADE, unique=False)
#     user_id = models.ForeignKey(User, on_delete=models.CASCADE, unique=False)

#     class Meta:
#         unique_together = ('event_id', 'user_id')
