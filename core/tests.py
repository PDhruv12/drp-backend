from django.test import TestCase
from .models import EventTable
from datetime import date, time

class SimpleTest(TestCase):
    def test_basic_math(self):
        self.assertEqual(1 + 1, 2)

# class EventModelTest(TestCase):

#     def setUp(self):
#         self.event = Event.objects.create(
#             title="Community Meetup",
#             image="https://example.com/image.jpg",
#             description="A friendly community gathering.",
#             location="Community Center",
#             host="Jane Doe",
#             signups=25,
#             distance=2.5,
#             date=date(2025, 6, 15),
#             time=time(18, 0),
#             accepted=True
#         )

#     def test_event_creation(self):
#         self.assertEqual(self.event.title, "Community Meetup")
#         self.assertEqual(self.event.image, "https://example.com/image.jpg")
#         self.assertEqual(self.event.description, "A friendly community gathering.")
#         self.assertEqual(self.event.location, "Community Center")
#         self.assertEqual(self.event.host, "Jane Doe")
#         self.assertEqual(self.event.signups, 25)
#         self.assertEqual(self.event.distance, 2.5)
#         self.assertEqual(self.event.date, date(2025, 6, 15))
#         self.assertEqual(self.event.time, time(18, 0))
#         self.assertTrue(self.event.accepted)

#     def test_string_representation(self):
#         self.assertEqual(str(self.event), "Community Meetup")