from rest_framework import serializers

from ..models import *


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"


class VolunteershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Volunteership
        fields = "__all__"
