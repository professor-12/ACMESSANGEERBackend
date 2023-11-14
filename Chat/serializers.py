from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *

class UserSerialiser(serializers.ModelSerializer):
      class Meta:
            model=User
            fields = ["username",  "first_name", "email","date_joined", "password"]



class ChatSerializer(serializers.ModelSerializer):
      class Meta:
            model=Chat
            fields = "__all__"
            
            
class ProfileSerializer(serializers.ModelSerializer):
      class Meta:
            model=Profile
            fields = "__all__"
            
            
class ContactSerializer(serializers.ModelSerializer):
      class Meta:
            model=Contacts
            fields = "__all__"