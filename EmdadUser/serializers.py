from rest_framework import serializers
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    class Meta:
        model = CustomUser
        fields = ['full_name', 'phone']

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"    