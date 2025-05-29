
from rest_framework import serializers
from .models import ExampleTableModel, Event

class ExampleTableModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExampleTableModel
        fields = '__all__' 

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'