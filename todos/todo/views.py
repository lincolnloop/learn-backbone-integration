from rest_framework import generics, permissions

from todos.todo.models import Category, Todo
from todos.todo.serializers import CategorySerializer, TodoSerializer


class CategoryList(generics.ListAPIView):
    model = Category
    serializer_class = CategorySerializer


class CategoryDetail(generics.RetrieveAPIView):
    model = Category
    serializer_class = CategorySerializer


class TodoList(generics.ListCreateAPIView):
    model = Todo
    serializer_class = TodoSerializer

    def get_queryset(self):
        return Todo.objects.filter(owner=self.request.user)

    def pre_save(self, obj):
        """Automatically provide the owner"""
        obj.owner = self.request.user


class IsOwner(permissions.BasePermission):
    """
    Check to make sure the current user is the owner.
    """

    def has_permission(self, request, view, obj=None):
        if obj:
            return request.user == getattr(obj, 'owner', None)
        return True


class TodoDetail(generics.RetrieveUpdateDestroyAPIView):
    model = Todo
    serializer_class = TodoSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwner)

    def pre_save(self, obj):
        """Automatically provide the owner"""
        obj.owner = self.request.user
