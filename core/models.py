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

class CommunityMessage(models.Model):
    TEXT = 'text'
    EVENT = 'event'

    MESSAGE_TYPE_CHOICES = [
        (TEXT, 'Text'),
        (EVENT, 'Event'),
    ]

    message_id = models.AutoField(primary_key=True)
    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(UserTable, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    message_type = models.CharField(max_length=10, choices=MESSAGE_TYPE_CHOICES, default=TEXT)
    text = models.TextField(blank=True, null=True)  # For text content (image is url so text)
    event = models.ForeignKey(EventTable, on_delete=models.SET_NULL, null=True, blank=True)  # For event shares

    class Meta:
        ordering = ['timestamp']

class CommunityMessageImage(models.Model):
    image_id = models.AutoField(primary_key=True)
    image = models.TextField()
    message = models.ForeignKey(CommunityMessage, on_delete=models.CASCADE, unique=False)

class UsersMessage(models.Model):
    TEXT = 'text'
    EVENT = 'event'

    MESSAGE_TYPE_CHOICES = [
        (TEXT, 'Text'),
        (EVENT, 'Event'),
    ]

    message_id = models.AutoField(primary_key=True)
    sender = models.ForeignKey(UserTable, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(UserTable, on_delete=models.CASCADE, related_name='received_messages')
    timestamp = models.DateTimeField(auto_now_add=True)

    message_type = models.CharField(max_length=10, choices=MESSAGE_TYPE_CHOICES, default=TEXT)
    text = models.TextField(blank=True, null=True) 
    event = models.ForeignKey(EventTable, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['timestamp']

class UsersMessageImage(models.Model):
    image_id = models.AutoField(primary_key=True)
    image = models.TextField()
    message = models.ForeignKey(UsersMessage, on_delete=models.CASCADE, related_name='images')

class Notification(models.Model):
    SAY_HI = 'say_hi'
    JOINED_COMMUNITY = 'joined_community'
    DM_MESSAGE = 'dm_message'
    COMMUNITY_MESSAGE = 'community_message'

    NOTIFICATION_TYPE_CHOICES = [
        (SAY_HI, 'Say Hi'),
        (JOINED_COMMUNITY, 'Joined Community'),
        (DM_MESSAGE, 'Direct Message'),
        (COMMUNITY_MESSAGE, 'Community Message'),
    ]

    notification_id = models.AutoField(primary_key=True)
    receiver = models.ForeignKey(UserTable, on_delete=models.CASCADE, related_name='notifications')
    sender = models.ForeignKey(UserTable, on_delete=models.SET_NULL, null=True, blank=True, related_name='sent_notifications')

    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPE_CHOICES)

    # Optional foreign keys to related objects depending on type
    community = models.ForeignKey(Community, on_delete=models.SET_NULL, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.notification_type} -> {self.receiver.name}"

# say hi, joined in community, message dm, message in community
