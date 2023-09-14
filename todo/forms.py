from django.forms import ModelForm, CharField
from todo.models import Todo


class TodoForm(ModelForm):
    
    description = CharField(required=False)
    
    class Meta:
        model = Todo
        fields = ('text', 'description')

class EditTodoForm(ModelForm):
    
    description = CharField(required=False)
    class Meta:
        model = Todo
        fields = ('text', 'description')
        labels = { 'text': '' }