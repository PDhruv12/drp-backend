from django.forms import model_to_dict
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import ExampleTableModel, EventSignUpModel
from .serializers import ExampleTableModelSerializer, EventSignUpModelSerializer

def my_api_endpoint(request):
  data = {'message': 'Hello from Django!'}
  return JsonResponse(data)

def alive(_):
  data = {'message': "yeah bro I'm still alive"}
  return JsonResponse(data)

# User sends post request with location
def get_data_from_db_orm(request):
  # This is a placeholder. You need to define YourTableModel in a models.py file.
  from .models import ExampleTableModel # Import your model
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

@api_view(['GET'])
def get_signups(request, event_id):
    try:
        event = EventSignUpModel.objects.get(eventId=event_id)
        serializer = EventSignUpModelSerializer(event)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except EventSignUpModel.DoesNotExist:
        return Response({'error': 'Event not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET', 'POST'])
def update_signups(request, event_id):
    try:
        event = EventSignUpModel.objects.get(eventId=event_id)
        if(event.signedUp == False):
          event.signUps += 1
          event.signedUp = True
        else:
          event.signUps -= 1
          event.signedUp = False
        event.save()
        serializer = EventSignUpModelSerializer(event)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    except EventSignUpModel.DoesNotExist:
        # Optionally create event if it doesn't exist
        event = EventSignUpModel.objects.create(eventId=event_id, signUps=1)
        serializer = EventSignUpModelSerializer(event)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET', 'POST'])
def add_events(request):
  id = request.query_params.get('id')
  num = request.query_params.get('num')
  new_record = EventSignUpModel.objects.create(eventId = id, signUps=num, signedUp = False)
  serializer = EventSignUpModelSerializer(new_record)
  return Response(serializer.data, status=status.HTTP_201_CREATED)