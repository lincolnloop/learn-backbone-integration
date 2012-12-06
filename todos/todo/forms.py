from django import forms

from todos.todo.models import Todo


class TodoForm(forms.ModelForm):

    class Meta:
        model = Todo
