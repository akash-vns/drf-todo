from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as DjUserAdmin
from todo.models import Todo
User = get_user_model()
# Register your models here.


class TodoInLine(admin.TabularInline):
    model = Todo
    extra = 1


class UserAdmin(DjUserAdmin):
    inlines = [TodoInLine]


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
