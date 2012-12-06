from functools import wraps
import json

from django.core import serializers
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.views.generic import View

from todos.todo.forms import TodoForm
from todos.todo.models import Category, Todo


class HttpResponseUnauthorized(HttpResponse):
    status_code = 401


def login_required(view_method):
    @wraps(view_method)
    def _wrapped_view_method(view, request, *args, **kwargs):
        if request.user.is_authenticated():
            return view_method(view, request, *args, **kwargs)
        else:
            return HttpResponseUnauthorized()
    return _wrapped_view_method


class APIView(View):
    """Base view for API-related views"""

    def render(self, data=None, error=False):
        if error:
            response = HttpResponseBadRequest
        else:
            response = HttpResponse
        return response(content=json.dumps(data),
                        content_type='application/json')

    def serialize(self, objects):
        """
        Use Django's built-in serializer to convert to json, and adjust the
        fields as necessary.
        """
        condensed = []
        for obj in serializers.serialize('python', objects):
            fields = self.adjust_fields(obj, obj['fields'])
            fields['id'] = obj['pk']  # Add the id
            condensed.append(fields)
        return condensed

    def adjust_fields(self, obj, fields):
        """Allow subclasses to alter fields during serialization"""
        return fields


class CategoryView(APIView):
    http_method_names = ['get']

    @login_required
    def get(self, request, pk=None):
        request.META["CSRF_COOKIE_USED"] = True  # Enable the CSRF cookie
        if pk:
            category = get_object_or_404(Category, pk=pk)
            return self.render(self.serialize([category])[0])
        categories = Category.objects.all()
        return self.render(self.serialize(categories))


class TodoView(APIView):
    http_method_names = ['get', 'post', 'put', 'delete']

    def adjust_fields(self, obj, fields):
        # Remove the owner, which is automatically handled by the app
        del fields['owner']

        # Add a link to the category
        fields['category'] = reverse('categories', args=[fields['category']])

        return fields

    @login_required
    def get(self, request, pk=None):
        request.META["CSRF_COOKIE_USED"] = True  # Enable the CSRF cookie
        if pk:
            todo = get_object_or_404(Todo, pk=pk, owner=request.user)
            return self.render(self.serialize([todo])[0])
        todos = Todo.objects.filter(owner=request.user)
        return self.render(self.serialize(todos))

    @login_required
    def post(self, request, pk=None):
        data = json.loads(request.body)
        data['owner'] = request.user.pk
        form = TodoForm(data=data)
        if form.is_valid():
            form.save()
            return self.render({'id': form.instance.pk})
        else:
            return self.render(form.errors, error=True)

    @login_required
    def put(self, request, pk):
        todo = get_object_or_404(Todo, pk=pk, owner=request.user)
        data = json.loads(request.body)
        data['owner'] = request.user.pk
        form = TodoForm(data=data, instance=todo)
        if form.is_valid():
            form.save()
            return self.render()
        else:
            return self.render(form.errors, error=True)

    @login_required
    def delete(self, request, pk):
        todo = get_object_or_404(Todo, pk=pk, owner=request.user)
        todo.delete()
        return self.render()
