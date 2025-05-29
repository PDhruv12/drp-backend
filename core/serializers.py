
from rest_framework import serializers
from .models import ExampleTableModel, EventSignUpModel

class ExampleTableModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExampleTableModel
        fields = '__all__' 

class EventSignUpModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventSignUpModel
        fields = '__all__'