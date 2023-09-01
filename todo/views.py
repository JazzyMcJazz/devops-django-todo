from django.shortcuts import render, reverse, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from todo.models import Todo
from todo.forms import TodoForm


def index(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('todo:todos'))
    else:
        return HttpResponseRedirect('/accounts/login')

def todos(request, pk=None):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/accounts/login')

    todo_form = TodoForm()

    if request.method == 'POST':
        todo_form = TodoForm(request.POST)
        if todo_form.is_valid():
            todo_form.instance.user = request.user
            todo_form.save()
            todo_form = None
            return HttpResponseRedirect(reverse('todo:todos'))

    if request.method == 'DELETE':
        todo = get_object_or_404(Todo, pk=pk)
        if todo.user == request.user:
            todo.delete()
        else:
            return PermissionDenied
        context = { 'todos': Todo.objects.all(), 'todo_form': todo_form }
        return render(request, 'todo/snippets/empty.html', context)

    if not todo_form:
        todo_form = TodoForm()

    todos = Todo.objects.filter(user=request.user)
    context = { 'todos': todos, 'todo_form': todo_form }
    return render(request, 'todo/index.html', context)
