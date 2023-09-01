from django.shortcuts import render, reverse, get_object_or_404
from django.http import HttpResponseRedirect
from todo.models import Todo
from todo.forms import TodoForm


def index(request):
    return HttpResponseRedirect(reverse('todo:todos'))

def todos(request, pk=None):
    todo_form = TodoForm()

    if request.method == 'POST':
        todo_form = TodoForm(request.POST)
        if todo_form.is_valid():
            todo_form.save()
            todo_form = None
            return HttpResponseRedirect(reverse('todo:todos'))

    if request.method == 'DELETE':
        todo = get_object_or_404(Todo, pk=pk)
        todo.delete()
        context = { 'todos': Todo.objects.all(), 'todo_form': todo_form }
        return render(request, 'todo/snippets/empty.html', context)

    if not todo_form:
        todo_form = TodoForm()

    context = { 'todos': Todo.objects.all(), 'todo_form': todo_form }
    return render(request, 'todo/index.html', context)
