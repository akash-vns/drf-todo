"""register cron tabs to schedule tasks"""
from .models import Todo, Notification


def notification_reminder():
    """fuc that help you to create notification"""
    todos = Todo.objects.all()
    for each_todo in todos:
        if each_todo.is_deadline_miss:
            Notification.create_notification(each_todo.user, each_todo)
