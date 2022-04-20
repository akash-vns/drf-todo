from django.contrib.admin.widgets import AdminSplitDateTime
from django import forms
from .models import Todo
from datetime import datetime
from django.contrib.auth import get_user_model
from django.utils.timezone import make_aware
from django.forms import TextInput, MultiWidget, DateTimeField


User = get_user_model()


class MinimalSplitDateTimeMultiWidget(MultiWidget):

    def __init__(self, widgets=None, attrs=None):
        if widgets is None:
            if attrs is None:
                attrs = {}
            date_attrs = attrs.copy()
            time_attrs = attrs.copy()

            date_attrs['type'] = 'date'
            time_attrs['type'] = 'time'

            widgets = [
                TextInput(attrs=date_attrs),
                TextInput(attrs=time_attrs),
            ]
        super().__init__(widgets, attrs)

    # nabbing from https://docs.djangoproject.com/en/3.1/ref/forms/widgets/#django.forms.MultiWidget.decompress
    def decompress(self, value):
        if value:
            return [value.date(), value.strftime('%H:%M')]
        return [None, None]

    def value_from_datadict(self, data, files, name):
        date_str, time_str = super().value_from_datadict(data, files, name)
        # DateField expects a single string that it can parse into a date.

        if date_str == time_str == '':
            return None

        if time_str == '':
            time_str = '00:00'

        my_datetime = datetime.strptime(date_str + ' ' + time_str, "%Y-%m-%d %H:%M")
        # making timezone aware
        return make_aware(my_datetime)


class TodoFilterForm(forms.Form):
    """ Todo filter for to filter object with relations """
    user = forms.ModelChoiceField(queryset=User.objects.all(), required=True)

    def filter_qs(self):
        user = self.cleaned_data.get("user")
        return Todo.objects.filter(user=user)


class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ["user", "title", "description", "schedule_at"]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super(TodoForm, self).__init__(*args, **kwargs)
        self.fields["schedule_at"].widget = MinimalSplitDateTimeMultiWidget()
