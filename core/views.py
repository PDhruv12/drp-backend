from django.forms import model_to_dict
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import ExampleTableModel, Event
from .serializers import ExampleTableModelSerializer, EventSerializer

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
        event = Event.objects.get(id=event_id)
        serializer = EventSerializer(event)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Event.DoesNotExist:
        return Response({'error': 'Event not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET', 'POST'])
def update_signups(request, event_id):
    try:
        event = Event.objects.get(eventId=event_id)
        if(event.signedUp == False):
          event.signUps += 1
          event.signedUp = True
        else:
          event.signUps -= 1
          event.signedUp = False
        event.save()
        data = {
            'id': str(record.id),
            'title': record.title,
            'image': record.image,
            'description': record.description,
            'location': record.location,
            'host': record.host,
            'signups': record.signups,
            'distance': record.distance,
            'date': record.date.strftime('%B %d, %Y'),    
            'time': record.time.strftime('%-I:%M %p'),  
            'accepted': record.accepted,
        }
        return Response(data, status=status.HTTP_200_OK)
    
    except Event.DoesNotExist:
        # Optionally create event if it doesn't exist
        record = Event.objects.create(eventId=event_id, signUps=1)
        data = {
            'id': str(record.id),
            'title': record.title,
            'image': record.image,
            'description': record.description,
            'location': record.location,
            'host': record.host,
            'signups': record.signups,
            'distance': record.distance,
            'date': record.date.strftime('%B %d, %Y'),    
            'time': record.time.strftime('%-I:%M %p'),  
            'accepted': record.accepted,
        }
        return Response(data, status=status.HTTP_201_CREATED)

# User sends post request with location
def get_events(request):
  # This is a placeholder. You need to define YourTableModel in a models.py file.
  from .models import Event # Import your model
  # Example: Fetch all records
  records = Event.objects.all()
  # Convert queryset to a list of dictionaries
  data = []
  for record in records:
      data.append({
          'id': str(record.id),
          'title': record.title,
          'image': record.image,
          'description': record.description,
          'location': record.location,
          'host': record.host,
          'signups': record.signups,
          'distance': record.distance,
          'date': record.date.strftime('%B %d, %Y'),    
          'time': record.time.strftime('%-I:%M %p'),  
          'accepted': record.accepted,
      })
  return JsonResponse(data, safe=False)

@api_view(['GET', 'POST'])
def add_events(request):
    title = request.query_params.get('title')
    image = request.query_params.get('image')
    description = request.query_params.get('description')
    location = request.query_params.get('location')
    host = request.query_params.get('host')
    signups = request.query_params.get('signups', 0)
    distance = request.query_params.get('distance')
    date = request.query_params.get('date')
    time = request.query_params.get('time')
    accepted = request.query_params.get('accepted', 'false').lower() == 'true'

    # Validate required fields minimally
    if not all([title, image, description, location, host, distance, date, time]):
        return Response({'error': 'Missing required fields.'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Convert signups and distance to proper types
    try:
        signups = int(signups)
        distance = float(distance)
    except ValueError:
        return Response({'error': 'Invalid signups or distance format.'}, status=status.HTTP_400_BAD_REQUEST)

    # Parse date and time fields (assuming 'YYYY-MM-DD' and 'HH:MM[:ss]' format)
    from datetime import datetime
    try:
        date_obj = datetime.strptime(date, '%d-%m-%Y').date()
        time_obj = datetime.strptime(time, '%H:%M').time()
    except ValueError:
        return Response({'error': 'Invalid date or time format. Date format: YYYY-MM-DD, Time format: HH:MM'}, status=status.HTTP_400_BAD_REQUEST)

    # Create the event record
    new_event = Event.objects.create(
        title=title,
        image=image,
        description=description,
        location=location,
        host=host,
        signups=signups,
        distance=distance,
        date=date_obj,
        time=time_obj,
        accepted=accepted,
    )
    
    serializer = EventSerializer(new_event)
    return Response(serializer.data, status=status.HTTP_201_CREATED)
@api_view(['DELETE'])
def delete_all_events(request):
    count, _ = Event.objects.all().delete()
    return Response({'message': f'{count} events deleted.'})