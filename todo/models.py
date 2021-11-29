from django.utils import timezone
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your models here.
class AbstractDateTimeModel(models.Model):
    """abstract Date time model for create and update time in models"""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Todo(AbstractDateTimeModel):
    """maintain User task (todo's)"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks")
    title = models.CharField(max_length=100)
    description = models.TextField()

    # schedule task time and date
    schedule_at = models.DateTimeField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} created by {self.user.username}"

    ##############
    # property's #
    ##############
    @property
    def is_deadline_miss(self):
        """check id schedule_at is greater then today date and task is still incomplete"""
        if self.is_completed is False and self.schedule_at:
            return self.schedule_at <= timezone.now()
        return self.is_completed


class Notification(AbstractDateTimeModel):
    """register notification"""
    todo = models.ForeignKey(Todo, on_delete=models.CASCADE, related_name="todo_notifications")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    description = models.CharField(max_length=150, default="Your task is missed to perform")  # setting default message
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {str(self.todo)} - {str(self.user)}"

    @classmethod
    def create_notification(cls, user, todo_task):
        """create notification task"""
        return cls.objects.create(user=user, todo=todo_task)
