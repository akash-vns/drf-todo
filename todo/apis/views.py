"""register Api's views"""
from rest_framework.mixins import UpdateModelMixin
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated
from todo.apis.serializers import TodoSerializer, NotificationSerializer
from todo.models import Todo


class TodoModelViewSet(ModelViewSet):
    """used to manage all todo's"""
    serializer_class = TodoSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        """update default context"""
        context = super(TodoModelViewSet, self).get_serializer_context()
        context['user'] = self.request.user
        return context

    def get_queryset(self):
        """return query related to current user"""
        return self.request.user.tasks.all()


class NotificationViewSet(UpdateModelMixin, ReadOnlyModelViewSet):
    """used to update and readonly serializer"""
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """return user's notifications"""
        return self.request.user.notifications.all()
