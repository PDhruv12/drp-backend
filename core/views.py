from django.forms import model_to_dict
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from models import ExampleTableModel
from serializers import ExampleTableModelSerializer

def my_api_endpoint(request):
  data = {'message': 'Hello from Django!'}
  return JsonResponse(data)

def alive(_):
  data = {'message': "yeah bro I'm still alive"}
  return JsonResponse(data)

# User sends post request with location
def get_data_from_db_orm(request):
  # This is a placeholder. You need to define YourTableModel in a models.py file.
  from models import ExampleTableModel # Import your model
  
  # Example: Fetch all records
  records = ExampleTableModel.objects.all()
  
  # Convert queryset to a list of dictionaries
  data = [model_to_dict(record) for record in records]
  return JsonResponse(data, safe=False)

@api_view(['GET', 'POST'])
def example_data_view(request):
  name1 = request.query_params.get('name')
  value1 = request.query_params.get('value')
  new_record = ExampleTableModel.objects.create(name=name1, value=value1)
  serializer = ExampleTableModelSerializer(new_record)
  return Response(serializer.data, status=status.HTTP_201_CREATED)
  # serializer = ExampleTableModelSerializer(data=request.data)
  # if serializer.is_valid():
  #   serializer.save()
  #   return Response(serializer.data, status=status.HTTP_201_CREATED)
  # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
