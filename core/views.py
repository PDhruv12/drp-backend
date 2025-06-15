from datetime import datetime
from django.utils import timezone
from django.forms import model_to_dict
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import EventTable, UserTable, EventImage, Attendee, Tag, Cohost
from .models import Community, CommunityImage, CommunityTag, CommunityMember, CommunityMessage, CommunityMessageImage
from .models import UsersMessage, UsersMessageImage
from .serializers import UserSerializer, EventImageSerializer, TagsSerializer
from django.db.models import Q

import logging
logger = logging.getLogger(__name__)

@api_view(['GET'])
def get_events_all(request, user_id):
    combined_data = []
    for event in EventTable.objects.all():
        combined_data.append(event_to_json(event.event_id, user_id))
    return Response(combined_data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_events(request, user_id):
    combined_data = []
    for event in EventTable.objects.all():
        if not event.over:
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
    price = data.get('price')
    image_urls = data.get('image_urls', [])
    tags = data.get('tags', [])
    cohosts = data.get('cohost', [])

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
        host_id=host,
        price=price
    )

    for url in image_urls:
        EventImage.objects.create(event=event, image=url)

    for tag in tags:
        Tag.objects.create(event=event, tag_name=tag)

    for cohost_id in cohosts:
        cohost = UserTable.objects.filter(user_id=cohost_id)
        if cohost.exists():
            Cohost.objects.create(event=event, host=cohost.first())

    return Response({"message": "Event created", "event_id": event.event_id}, status=status.HTTP_201_CREATED)

# ___________________________________________________________________________________________

@api_view(['GET'])
def users(request):
    records = UserTable.objects.all()
    serializer = UserSerializer(records, many=True)
    return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)

@api_view(['GET', 'POST'])
def add_user(request):
    data = request.data
    user_id = data.get('user')
    name = data.get('name')
    password_hash = data.get('pass')
    date_of_birth = data.get('dob')
    description = data.get('description')

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

@api_view(['POST'])
def login(request):
    data = request.data
    user_id = data.get('user')
    to_check = data.get('pass')
    pass_hash = UserTable.objects.filter(user_id=user_id)
    if not pass_hash.exists():
        return Response({'error': 'User ID does not exist.'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        hash = pass_hash.first()
        if hash.password_hash == to_check:
            return Response({'Valid User': "Authorized"}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Password wrong.'}, status=status.HTTP_400_BAD_REQUEST)

def event_to_json(event_id, user_id):
    event = EventTable.objects.get(event_id = event_id)
    image_obj = EventImage.objects.filter(event = event.event_id)
    host_info = UserTable.objects.get(user_id = event.host_id.user_id)
    attendees = Attendee.objects.filter(event = event.event_id)
    accepted = attendees.filter(user = user_id).exists()
    tags = Tag.objects.filter(event=event.event_id)
    cohosts = Cohost.objects.filter(event=event)

    if not image_obj.exists():
        img = ['https://picsum.photos/seed/potluck/200/200']
    else:
        img = [image_entry.image for image_entry in image_obj]
    
    if not tags.exists():
        tag = []
    else:
        tag = [tag_entry.tag_name for tag_entry in tags]

    if not cohosts.exists():
        cohost = []
    else:
        cohost = [
            model_to_dict(cohost_entry.host, fields=['user_id', 'name', 'date_of_birth', 'description']) 
            for cohost_entry in cohosts]

    now = timezone.localtime(timezone.now()).replace(second=0, microsecond=0)
    # Combine event date and end time, then make it aware using London time
    event_end_naive = datetime.combine(event.date, event.end_time).replace(second=0, microsecond=0)
    # Make aware only if needed
    if timezone.is_naive(event_end_naive):
        event_end_aware = timezone.make_aware(event_end_naive, timezone.get_default_timezone())
    else:
        event_end_aware = event_end_naive

    # Compare
    if event_end_aware <= now:
        event.over = True
        event.save()


    return {
        "id": event.event_id,
        "title": event.title,
        "image": img,
        "description": event.description,
        "location": event.location,
        "host": host_info.name,
        "host_id": host_info.user_id,
        "cohost": cohost,
        "tags": tag,
        "signups": attendees.count(),
        "distance": event.distance,
        "date": event.date.strftime('%B %d, %Y'),
        "time": event.start_time.strftime('%-I:%M %p'),
        "end_time": event.end_time.strftime('%-I:%M %p'),
        "price": event.price,
        "accepted": accepted,
        "over": event.over,
    }

# ____________________________________________________________________________________________

@api_view(['DELETE', 'GET'])
def delete_all_events(request):
    count, _ = EventTable.objects.all().delete()
    return Response({'message': f'{count} events deleted.'})

@api_view(['GET'])
def delete_particular_event(request, event_id):
    EventTable.objects.get(event_id = event_id).delete()

@api_view(['GET'])
def view_images(request):
    records = EventImage.objects.all()
    serializer = EventImageSerializer(records, many=True)
    return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)

@api_view(['GET'])
def getTags(request):
    records = Tag.objects.all()
    serializer = TagsSerializer(records, many=True)
    return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)

# ____________________________________________________________________________________

@api_view(['POST'])
def add_community(request, user_id):
    data = request.data
    
    # Extract individual fields
    name = data.get('name')
    description = data.get('description')
    image_urls = data.get('image_urls', [])
    tags = data.get('tags', [])
    members_id = data.get('members')

    if not all([name, description]):
        return Response({"error": "Missing required fields"}, status=status.HTTP_400_BAD_REQUEST)

    community = Community.objects.create(
        name=name,
        description=description,
    )

    for url in image_urls:
        CommunityImage.objects.create(community=community, image=url)

    for tag in tags:
        CommunityTag.objects.create(community=community, tag_name=tag)

    for member in members_id:
        user = UserTable.objects.filter(user_id=member)
        if user.exists():
            CommunityMember.objects.create(community=community, user=user.first())

    user = UserTable.objects.get(user_id=user_id)
    if not CommunityMember.objects.filter(community=community, user=user).exists():
        CommunityMember.objects.create(community=community, user=user)

    return Response({"message": "Community created", "community_id": community.community_id}, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def get_communities(request, user_id):
    combined_data = []
    for community in Community.objects.all():
        combined_data.append(community_to_json(community.community_id, user_id))
    return Response(combined_data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_my_communities(request, user_id):
    combined_data = []
    user = UserTable.objects.get(user_id=user_id)
    communities = CommunityMember.objects.filter(user=user)
    for community in Community.objects.all():
        if communities.filter(community=community).exists():
            combined_data.append(community_to_json(community.community_id, user_id))
    return Response(combined_data, status=status.HTTP_200_OK)

def get_particular_community(request, user_id, community_id):
    return Response(community_to_json(community_id, user_id), status=status.HTTP_200_OK)

def community_to_json(community_id, user_id):
    community = Community.objects.get(community_id=community_id)
    image_obj = CommunityImage.objects.filter(community=community)
    tags = CommunityTag.objects.filter(community=community)
    members = CommunityMember.objects.filter(community=community)
    
    if not image_obj.exists():
        img = ['https://picsum.photos/seed/fire/200/200']
    else:
        img = [image_entry.image for image_entry in image_obj]
    
    if not tags.exists():
        tag = []
    else:
        tag = [tag_entry.tag_name for tag_entry in tags]
    
    member = []
    if members.exists():
        for member_entry in members:
            user_dict = model_to_dict(member_entry.user, fields=['name', 'date_of_birth', 'description'])
            user_dict['user_id'] = member_entry.user.user_id
            member.append(user_dict)

    return {
        "id": community.community_id,
        "name": community.name,
        "description": community.description,
        "tags": tag,
        "image": img,
        "members": member,
    }

# ____________________________________________________________________________________________________________

@api_view(['GET', 'POST'])
def get_messages(request, user_id):
    data = request.data
    community_id = data.get('community')
    community = Community.objects.get(community_id=community_id)
    combined_data = []
    for message in CommunityMessage.objects.filter(community=community):
        combined_data.append(message_to_json(message.message_id, user_id))
    return Response(combined_data, status=status.HTTP_200_OK)

@api_view(['POST'])
def send_message(request, user_id):
    data = request.data
    community_id = data.get('community')
    community = Community.objects.get(community_id=community_id)
    sender = UserTable.objects.get(user_id=user_id)
    message_type = data.get('message_type')
    text = data.get('text')
    event_id = data.get('event')
    images = data.get('image', [])
    if message_type == 'text':
        message = CommunityMessage.objects.create(
            community = community,
            sender = sender,
            message_type = message_type,
            text = text,
        )
    elif message_type == 'event':
        event = EventTable.objects.get(event_id=event_id)
        message = CommunityMessage.objects.create(
            community = community,
            sender = sender,
            message_type = message_type,
            event = event,
        )
    else:
        return Response({}, status=status.HTTP_400_BAD_REQUEST)
    
    for image in images:
        CommunityMessageImage.objects.create(image=image, message=message)
    
    return Response(message_to_json(message.message_id, user_id), status=status.HTTP_201_CREATED)


def message_to_json(message_id, user_id):
    message = CommunityMessage.objects.get(message_id=message_id)
    event = ""
    text = ""
    images = CommunityMessageImage.objects.filter(message=message)
    if message.message_type == 'event': 
        event = event_to_json(message.event.event_id, user_id)
    elif message.message_type == 'text':
        text = message.text
    
    img = []
    for image in images:
        img.append(image.image)

    sender_data = {
        "name": message.sender.name,
        "user_id": message.sender.user_id
    }
    return {
        "message_id": message.message_id,
        "sender": sender_data,
        "message_type": message.message_type,
        "text": text,
        "event": event, 
        "image": img,
        "date": message.timestamp.strftime('%d %B, %Y'),
        "time": message.timestamp.strftime('%-I:%M %p'),
        "user": message.sender.user_id,
        "name": message.sender.name,
    }

@api_view(['GET'])
def add_community_from_browser(request, user_id, name, description):
    community = Community.objects.create(
        name=name, description=description
    )
    return Response(community_to_json(community.community_id, user_id), status=status.HTTP_200_OK)

@api_view(['GET'])
def make_member(request, user_id, community_id):
    user = UserTable.objects.get(user_id=user_id)
    community = Community.objects.get(community_id=community_id)
    if not CommunityMember.objects.filter(community=community, user=user).exists():
        CommunityMember.objects.create(community=community, user=user)
    return Response({"message": "Community member"}, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def delete_community(request, community_id):
    Community.objects.get(community_id=community_id).delete()

#___________________________________USER MSG__________________________________

@api_view(['POST'])
def send_user_message(request, user_id):
    data=request.data
    sender = UserTable.objects.get(user_id=user_id)
    receiver_id = data.get('receiver')
    receiver = UserTable.objects.get(user_id=receiver_id)
    message_type = data.get('message_type')
    text = data.get('text')
    event_id = data.get('event')
    images = data.get('image', [])

    if message_type == 'text':
        message = UsersMessage.objects.create(
            sender=sender,
            receiver=receiver,
            message_type=message_type,
            text=text
        )
    elif message_type == 'event':
        event = EventTable.objects.get(event_id=event_id)
        message = CommunityMessage.objects.create(
            sender=sender,
            receiver=receiver,
            message_type=message_type,
            event=event
        )
    else:
        return Response({}, status=status.HTTP_400_BAD_REQUEST)
    
    for image in images:
        UsersMessageImage.objects.create(image=image, message=message)
    
    return Response(user_message_to_json(message.message_id, user_id), status=status.HTTP_201_CREATED)

@api_view(['GET', 'POST'])
def user_messages(request, user_id):
    data = request.data
    user2_id = data.get('other_user')
    user = UserTable.objects.get(user_id=user_id)
    user2 = UserTable.objects.get(user_id=user2_id)
    messages = UsersMessage.objects.filter(
            Q(sender=user, receiver=user2) |
            Q(sender=user2, receiver=user)
        ).order_by('timestamp')
    
    combined_data = []
    for message in messages:
        combined_data.append(user_message_to_json(message.message_id, user_id))
    return 

def user_message_to_json(message_id, user_id):
    message = UsersMessage.objects.get(message_id=message_id)
    event = ""
    text = ""
    images = UsersMessageImage.objects.filter(message=message)
    if message.message_type == 'event': 
        event = event_to_json(message.event.event_id, user_id)
    elif message.message_type == 'text':
        text = message.text
    
    img = []
    for image in images:
        img.append(image.image)

    sender_data = {
        "name": message.sender.name,
        "user_id": message.sender.user_id
    }
    receiver_data = {
        "name": message.receiver.name,
        "user_id": message.receiver.user_id
    }
    return {
        "message_id": message.message_id,
        "sender": sender_data,
        "receiver": receiver_data,
        "message_type": message.message_type,
        "text": text,
        "event": event, 
        "image": img,
        "date": message.timestamp.strftime('%d %B, %Y'),
        "time": message.timestamp.strftime('%-I:%M %p'),
    }
