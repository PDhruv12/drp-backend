
from rest_framework import serializers
from .models import UserTable, EventTable, EventImage, Tag, Cohost

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
        model = UserTable
        fields = ['user_id', 'name', 'password_hash', 'date_of_birth', 'description']

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventTable
        fields = '__all__'


class EventImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventImage
        fields = '__all__'

class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class CohostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cohost
        fields = '__all__'