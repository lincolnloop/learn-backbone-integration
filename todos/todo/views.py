from functools import wraps
import json

from django.core import serializers
from django.http import HttpResponse, HttpResponseBadRequest, Http404
from django.shortcuts import get_object_or_404
from django.views.generic import View

from todos.todo.forms import TodoForm
from todos.todo.models import Todo


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


class TodoView(View):
    http_method_names = ['get', 'post', 'put', 'delete']

    def render(self, data=None, error=False):
        if error:
            response = HttpResponseBadRequest
        else:
            response = HttpResponse
        return response(content=json.dumps(data),
                        content_type='application/json')

    def serialize(self, queryset):
        """
        Use Django's built-in serializer to convert to json, and adjust the
        fields as necessary.
        """
        condensed = []
        for obj in serializers.serialize('python', queryset):
            fields = obj['fields']

            # Remove the owner, which is automatically handled by the app
            del fields['owner']

            # Add the id
            fields['id'] = obj['pk']

            condensed.append(fields)
        return condensed

    @login_required
    def get(self, request, pk=None):
        request.META["CSRF_COOKIE_USED"] = True  # Enable the CSRF cookie
        if pk:
            todos = Todo.objects.filter(pk=pk, owner=request.user)
            if not todos:
                raise Http404
        else:
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
