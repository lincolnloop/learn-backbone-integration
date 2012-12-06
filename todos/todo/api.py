from tastypie import http
from tastypie.authentication import SessionAuthentication
from tastypie.authorization import Authorization
from tastypie.resources import ModelResource
from tastypie.utils import dict_strip_unicode_keys

from todos.todo.models import Todo


class TodoResource(ModelResource):

    class Meta:
        queryset = Todo.objects.all()
        resource_name = 'todos'
        always_return_data = True
        authentication = SessionAuthentication()
        authorization = Authorization()

    def apply_authorization_limits(self, request, object_list):
        return object_list.filter(owner=request.user)

    def obj_create(self, bundle, request=None, **kwargs):
        return super(TodoResource, self).obj_create(
            bundle, request, owner=request.user, **kwargs
        )

    def put_detail(self, request, **kwargs):
        """
        Override this to avoid falling back on obj_create, which would
        effectively allow users to update Todos they don't own.
        """
        deserialized = self.deserialize(request, request.raw_post_data, format=request.META.get('CONTENT_TYPE', 'application/json'))
        deserialized = self.alter_deserialized_detail_data(request, deserialized)
        bundle = self.build_bundle(data=dict_strip_unicode_keys(deserialized), request=request)

        updated_bundle = self.obj_update(bundle, request=request, **self.remove_api_resource_names(kwargs))

        if not self._meta.always_return_data:
            return http.HttpNoContent()
        else:
            updated_bundle = self.full_dehydrate(updated_bundle)
            updated_bundle = self.alter_detail_data_to_serialize(request, updated_bundle)
            return self.create_response(request, updated_bundle, response_class=http.HttpAccepted)
