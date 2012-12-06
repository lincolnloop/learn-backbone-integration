from rest_framework import serializers

from todos.todo.models import Todo


class TodoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Todo
        fields = ('id', 'title', 'order', 'done')
