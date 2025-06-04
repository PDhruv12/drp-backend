from datetime import datetime
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import EventTable, UserTable, EventImage, Attendee
from .serializers import UserSerializer, EventImageSerializer

import logging
logger = logging.getLogger(__name__)

@api_view(['GET'])
def get_events(request, user_id):
    combined_data = []
    for event in EventTable.objects.all():
        combined_data.append(event_to_json(event.event_id, user_id))
    return Response(combined_data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_event(request, user_id, event_id):
    return Response(event_to_json(event_id, user_id), status=status.HTTP_200_OK)

@api_view(['GET', 'POST'])
def event_sign_up(request, user_id, event_id):
    try:
        event = EventTable.objects.get(event_id = event_id)
        user_info = UserTable.objects.get(user_id = user_id)
        attendee_exists = Attendee.objects.filter(event = event, user=user_info).exists()
        if not attendee_exists:
            Attendee.objects.create(event = event, user=user_info)
        else:
            Attendee.objects.filter(event=event, user=user_info).delete()
        return Response(event_to_json(event_id, user_id), status=status.HTTP_200_OK)

    except EventTable.DoesNotExist:
        return Response({"detail": "Event not found."},status=status.HTTP_404_NOT_FOUND)
    except UserTable.DoesNotExist:
        return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def add_event(request, user_id):
    data = request.data
    logger.info(f"POST data from user {user_id}: {request.data}")
    # Extract individual fields
    title = data.get('title')
    date = data.get('date')
    start_time = data.get('start_time')
    end_time = data.get('end_time')
    location = data.get('location')
    description = data.get('description')
    host_id = data.get('host_id')
    image_urls = data.get('image_urls', [])

    if not all([title, date, start_time, location, description, host_id]):
        return Response({"error": "Missing required fields"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        host = UserTable.objects.get(user_id=host_id)
    except UserTable.DoesNotExist:
        return Response({"error": "Host user does not exist"}, status=status.HTTP_400_BAD_REQUEST)
    
    event = EventTable.objects.create(
        title=title,
        date=date,
        start_time=start_time,
        end_time=end_time,
        location=location,
        description=description,
        host_id=host
    )

    for url in image_urls:
        EventImage.objects.create(event_id=event, image=url)

    return Response({"message": "Event created", "event_id": event.event_id}, status=status.HTTP_201_CREATED)

# ___________________________________________________________________________________________

@api_view(['GET'])
def users(request):
    records = UserTable.objects.all()
    serializer = UserSerializer(records, many=True)
    return JsonResponse(serializer.data, status=status.HTTP_200_OK)

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
    if not all([user_id, name, password_hash, date_of_birth, description]):
        return Response({'error': 'Missing required fields.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        date_obj = datetime.strptime(date_of_birth, '%d-%m-%Y').date()
    except ValueError:
        return Response({'error': 'Invalid date format. Date format: DD-MM-YYYY'}, status=status.HTTP_400_BAD_REQUEST)

    if UserTable.objects.filter(user_id=user_id).exists():
        return Response({'error': 'User ID already exists.'}, status=status.HTTP_400_BAD_REQUEST)

    new_user = UserTable.objects.create(
        user_id=user_id,
        name=name,
        password_hash=password_hash,
        date_of_birth=date_obj,
        description=description
    )
    serializer = UserSerializer(new_user)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

def event_to_json(event_id, user_id):
    event = EventTable.objects.get(event_id = event_id)
    image_obj = EventImage.objects.filter(event = event.event_id)
    host_info = UserTable.objects.get(user_id = event.host_id.user_id).name
    attendees = Attendee.objects.filter(event = event.event_id)
    accepted = attendees.filter(user = user_id).exists()
    if not image_obj.exists():
        img = 'https://picsum.photos/seed/potluck/200/200'
    else:
        img = image_obj.first().image
    return {
        "id": event.event_id,
        "title": event.title,
        "image": img,
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

@api_view(['DELETE', 'GET'])
def delete_all_events(request):
    count, _ = EventTable.objects.all().delete()
    return Response({'message': f'{count} events deleted.'})

@api_view(['GET'])
def view_images(request):
    records = EventImage.objects.all()
    serializer = EventImageSerializer(records, many=True)
    return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)
