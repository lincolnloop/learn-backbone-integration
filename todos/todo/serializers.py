from rest_framework import serializers
from rest_framework.fields import Field

from todos.todo.models import Category, Todo


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    id = Field()

    class Meta:
        model = Category
        fields = ('id', 'title')


class TodoSerializer(serializers.HyperlinkedModelSerializer):
    id = Field()

    class Meta:
        model = Todo
        fields = ('id', 'title', 'order', 'done', 'category')
