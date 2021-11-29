"""register serializes"""
from rest_framework import serializers
from todo.models import Todo, Notification


class TodoSerializer(serializers.ModelSerializer):
    """todo model related serializer"""

    class Meta:
        model = Todo
        fields = ['title', 'description', "schedule_at", "is_completed", 'created_at', 'updated_at', 'id']
        read_only_fields = ["created_at", "updated_at"]

    def create(self, validated_data):
        # add user to validate data to create current user task
        validated_data['user'] = self.context["user"]
        return super(TodoSerializer, self).create(validated_data)


class NotificationSerializer(serializers.ModelSerializer):
    """Notification model related serializer"""
    class Meta:
        model = Notification
        fields = ['user', "todo", "created_at", "updated_at", "is_read", 'id']
        read_only_fields = ["created_at", "updated_at", "user", "todo"]
