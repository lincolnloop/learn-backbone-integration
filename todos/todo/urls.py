from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic.simple import direct_to_template

from todos.todo.api import CategoryResource, TodoResource

admin.autodiscover()

todo_resource = TodoResource()
category_resource = CategoryResource()


urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', direct_to_template, {'template': 'index.html'}),

    (r'^', include(category_resource.urls)),
    (r'^', include(todo_resource.urls)),
)
