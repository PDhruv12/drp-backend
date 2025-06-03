
from rest_framework import serializers
from .models import User

# class EventSerializer(serializers.ModelSerializer):
#     # Format date and time fields as strings
#     date = serializers.SerializerMethodField()
#     time = serializers.SerializerMethodField()

#     class Meta:
#         model = Event
#         fields = [
#             'id', 'title', 'image', 'description', 'location',
#             'host', 'signups', 'distance', 'date', 'time', 'accepted'
#         ]

#     def get_date(self, obj):
#         return obj.date.strftime('%B %d, %Y')

#     def get_time(self, obj):
#         return obj.time.strftime('%I:%M %p').lstrip('0')
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'name', 'password_hash', 'date_of_birth', 'description']

