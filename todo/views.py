from django.shortcuts import render
from django.urls import reverse_lazy
from .forms import TodoFilterForm, TodoForm
from .models import Todo
from django.views.generic import ListView, UpdateView, CreateView
from django.contrib import messages
# Create your views here.


class TodoListView(ListView):
    template_name = "todo/todo_lists.html"
    queryset = Todo.objects.all()
    context_object_name = "todos"
    form_class = TodoFilterForm
    paginate_by = 1

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super(TodoListView, self).get_context_data(*args, **kwargs)
        context["filter_form"] = self.get_filter_form()
        return context

    def get_filter_form(self):
        data = self.request.GET if len(self.request.GET.keys()) > 0 else None
        if len(self.request.GET.keys()) == 1 and self.request.GET.get("page"):
            # handle page parameters
            data = None
        return self.form_class(data=data)

    def get_queryset(self):
        qs = super(TodoListView, self).get_queryset()
        filter_form = self.get_filter_form()
        if filter_form.is_bound and filter_form.is_valid():
            qs = filter_form.filter_qs()
        return qs


class FormErrorMessageMixin:
    success_message = "Data successfully submitted"
    error_message = "Please correct error below."

    def form_valid(self, form):
        messages.success(self.request, self.success_message)
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, self.error_message)
        return super().form_invalid(form)


class TodoUpdateView(FormErrorMessageMixin, UpdateView):
    """update family member details"""
    form_class = TodoForm
    template_name = "todo/update.html"
    queryset = Todo.objects.all()
    success_url = reverse_lazy("todo:todos")

    def get_form_kwargs(self):
        context = super().get_form_kwargs()
        context.update({"user": self.request.user})
        return context


class TodoCreateView(FormErrorMessageMixin, CreateView):
    """Create family members"""
    form_class = TodoForm
    template_name = "todo/create.html"
    success_url = reverse_lazy("todo:todos")

    def get_form_kwargs(self):
        context = super().get_form_kwargs()
        context.update({"user": self.request.user})
        return context
