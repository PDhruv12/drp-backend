from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import EventTable, UserTable, EventImage, Attendee
from .serializers import UserSerializer

@api_view(['GET'])
def get_events(request, user_id):
    combined_data = []
    for event in EventTable.objects.all():
        combined_data.append(event_to_json(event.event_id, user_id))
    return Response(combined_data, safe=False, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_event(request, user_id, event_id):
    return Response(event_to_json(event_id, user_id), status=status.HTTP_200_OK)

@api_view(['GET', 'POST'])
def event_sign_up(requets, user_id, event_id):
    try:
        attendee_exists = Attendee.objects.filter(event_id = event_id, user_id=user_id).exists()
        if not attendee_exists:
            Attendee.objects.create(event_id=event_id, user_id=user_id)
        return Response(event_to_json(event_id, user_id), status=status.HTTP_200_OK)

    except EventTable.DoesNotExist:
        return Response({"detail": "Event not found."},status=status.HTTP_404_NOT_FOUND)

# ___________________________________________________________________________________________

@api_view(['GET'])
def users(request):
    records = UserTable.objects.all()
    serializer = UserSerializer(records, many=True)
    return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)

@api_view(['GET', 'POST'])
def add_user(request):
    # user_id = request.query_params.get('user')
    # name = request.query_params.get('name')
    # password_hash = request.query_params.get('pass')
    # date_of_birth = request.query_params.get('dob')
    # description = request.query_params.get('description')
    user_id = 'user123'
    name = 'name'
    password_hash = 'pass'
    date_of_birth = '01-01-2001'
    description = 'description'
    # Validate required fields minimally
    if not all([user_id, name, description, password_hash, date_of_birth]):
        return Response({'error': 'Missing required fields.'}, status=status.HTTP_400_BAD_REQUEST)
    
    from datetime import datetime
    try:
        date_obj = datetime.strptime(date_of_birth, '%d-%m-%Y').date()
    except ValueError:
        return Response({'error': 'Invalid date or time format. Date format: YYYY-MM-DD, Time format: HH:MM'}, status=status.HTTP_400_BAD_REQUEST)

    # Create the event record
    new_user = UserTable.objects.create(
        user_id = user_id,
        name = name,
        password_hash = password_hash,
        date_of_birth = date_obj,
        description = description
    )
    serializer = UserSerializer(new_user)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

def event_to_json(event_id, user_id):
    event = EventTable.objects.get(event_id = event_id)
    image_obj = EventImage.objects.filter(event_id = event.event_id).first().image
    host_info = UserTable.objects.get(user_id = event.host_id).name
    attendees = Attendee.objects.filter(event_id = event.event_id)
    accepted = attendees.get(event_id=event_id, user_id = user_id)
    return {
        "id": event.event_id,
        "title": event.title,
        "image": image_obj,
        "description": event.description,
        "location": event.location,
        "host": host_info,
        "signups": attendees.count(),
        "distance": 1.2,
        "date": event.date.strftime('%B %d, %Y'),
        "time": event.start_time.strftime('%-I:%M %p'),
        "end_time": event.end_time.strftime('%-I:%M %p'),
        "accepted": accepted
    }

# ____________________________________________________________________________________________

# @api_view(['GET'])
# def get_signups(request, event_id):
#     try:
#         event = Event.objects.get(id=event_id)
#         serializer = EventSerializer(event)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     except Event.DoesNotExist:
#         return Response({'error': 'Event not found'}, status=status.HTTP_404_NOT_FOUND)

# @api_view(['GET', 'POST'])
# def update_signups(request, event_id):
#     try:
#         event = Event.objects.get(id=event_id)

#         if not event.accepted:
#             event.signups += 1
#             event.accepted = True
#         else:
#             event.signups -= 1
#             event.accepted = False
#         event.save()
#         serializer = EventSerializer(event)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     except Event.DoesNotExist:
#         return Response(
#             {"detail": "Event not found."},
#             status=status.HTTP_404_NOT_FOUND
#         )

# def get_events(request):
#     records = Event.objects.all()
#     serializer = EventSerializer(records, many=True)
#     return JsonResponse(serializer.data, safe=False)

# @api_view(['GET', 'POST'])
# def add_events(request):
#     title = request.query_params.get('title')
#     image = request.query_params.get('image')
#     description = request.query_params.get('description')
#     location = request.query_params.get('location')
#     host = request.query_params.get('host')
#     signups = request.query_params.get('signups', 0)
#     distance = request.query_params.get('distance')
#     date = request.query_params.get('date')
#     time = request.query_params.get('time')
#     accepted = request.query_params.get('accepted', 'false').lower() == 'true'

#     # Validate required fields minimally
#     if not all([title, image, description, location, host, distance, date, time]):
#         return Response({'error': 'Missing required fields.'}, status=status.HTTP_400_BAD_REQUEST)
    
#     # Convert signups and distance to proper types
#     try:
#         signups = int(signups)
#         distance = float(distance)
#     except ValueError:
#         return Response({'error': 'Invalid signups or distance format.'}, status=status.HTTP_400_BAD_REQUEST)

#     # Parse date and time fields (assuming 'YYYY-MM-DD' and 'HH:MM[:ss]' format)
#     from datetime import datetime
#     try:
#         date_obj = datetime.strptime(date, '%d-%m-%Y').date()
#         time_obj = datetime.strptime(time, '%H:%M').time()
#     except ValueError:
#         return Response({'error': 'Invalid date or time format. Date format: YYYY-MM-DD, Time format: HH:MM'}, status=status.HTTP_400_BAD_REQUEST)

#     # Create the event record
#     new_event = Event.objects.create(
#         title=title,
#         image=image,
#         description=description,
#         location=location,
#         host=host,
#         signups=signups,
#         distance=distance,
#         date=date_obj,
#         time=time_obj,
#         accepted=accepted,
#     )
    
#     serializer = EventSerializer(new_event)
#     return Response(serializer.data, status=status.HTTP_201_CREATED)

# @api_view(['DELETE', 'GET'])
# def delete_all_events(request):
#     count, _ = Event.objects.all().delete()
#     return Response({'message': f'{count} events deleted.'})