
from rest_framework import serializers
from .models import ExampleTableModel, Event

class ExampleTableModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExampleTableModel
        fields = '__all__' 

class EventSerializer(serializers.ModelSerializer):
    # Format date and time fields as strings
    date = serializers.SerializerMethodField()
    time = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = [
            'id', 'title', 'image', 'description', 'location',
            'host', 'signups', 'distance', 'date', 'time', 'accepted'
        ]

    def get_date(self, obj):
        return obj.date.strftime('%B %d, %Y')

    def get_time(self, obj):
        return obj.time.strftime('%I:%M %p').lstrip('0')