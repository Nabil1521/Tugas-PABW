from rest_framework import serializers
from .models import Car


class CarSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Car
        fields = ['id', 'carname', 'carbrand', 'carmodel', 'carprice']
