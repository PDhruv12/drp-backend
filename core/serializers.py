
from rest_framework import serializers
from models import ExampleTableModel

class ExampleTableModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExampleTableModel
        fields = '__all__'  # or ['id', 'name', 'location']