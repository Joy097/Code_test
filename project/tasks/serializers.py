from rest_framework import serializers
from .models import Task

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'