from django.shortcuts import render, reverse, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from todo.models import Todo
from todo.forms import TodoForm, EditTodoForm


def index():
    return HttpResponseRedirect(reverse('todo:todos'))
    
    
@login_required
def todos(request, pk=None):
    todo_form = TodoForm()

    if request.method == 'POST':
        todo_form = TodoForm(request.POST)
        if todo_form.is_valid():
            todo_form.instance.user = request.user
            if todo_form.instance.description == '':
                todo_form.instance.description = None
            todo_form.save()
            todo_form = None

    if request.method == 'DELETE':
        todo = get_object_or_404(Todo, pk=pk)
        if todo.user == request.user:
            todo.delete()
        else:
            raise PermissionDenied("This is not your todo!")
        return HttpResponse()
    
    if request.method == 'PATCH':
        todo = get_object_or_404(Todo, pk=pk)
        if todo.user == request.user:
            edit_form = EditTodoForm(request.PATCH, instance=todo)
            if edit_form.is_valid():
                edit_form.save()
                edit_form = None
        else:
            raise PermissionDenied("This is not your todo!")
        context = { 'todo': todo }
        return render(request, 'todo/partial/todo.html', context)

    if not todo_form:
        todo_form = TodoForm()

    todos = Todo.objects.filter(user=request.user)
    context = { 'todos': todos, 'todo_form': todo_form }

    return render(request, 'todo/index.html', context)

@login_required
def todos_edit_form(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    edit_form = EditTodoForm(initial={'text': todo.text, 'description': todo.description})
    context = { 'pk': pk, 'edit_form': edit_form }
    return render(request, 'todo/partial/edit-form.html', context)

