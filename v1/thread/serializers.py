from rest_framework import serializers
from .models import ChatThread


class ThreadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatThread
        fields = '__all__'
        read_only_fields = ('uuid', 'created')
