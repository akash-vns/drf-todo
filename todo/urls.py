from django.urls import path, include
from .views import TodoListView, TodoCreateView, TodoUpdateView

app_name = "todo"

urlpatterns = [
    path('api/', include('todo.apis.urls')),
    path("todos", TodoListView.as_view(), name="todos"),
    path("todo-create", TodoCreateView.as_view(), name="todo_create"),
    path("todo-update/<int:pk>", TodoUpdateView.as_view(), name="todo_update"),

]
