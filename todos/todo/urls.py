from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView

from todos.todo.api import CategoryResource, TodoResource

admin.autodiscover()

todo_resource = TodoResource()
category_resource = CategoryResource()


urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', TemplateView.as_view(template_name="index.html")),

    (r'^', include(category_resource.urls)),
    (r'^', include(todo_resource.urls)),
)
