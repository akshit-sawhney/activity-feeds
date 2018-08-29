from django.db import models
from mongoengine import *
from django.utils import timezone

connect('budgetmanager')
# Create your models here.

class Activity_feed(DynamicDocument):
    user_id = IntField(required=True)
    type = StringField(max_length=50)
    created_at = DateTimeField(default=timezone.now)


class User_activity_feed(Document):
    user_id = IntField(required=True)
    reference_id = ReferenceField(Activity_feed)
    relevance = IntField()
    created_at = DateTimeField(default=timezone.now)
