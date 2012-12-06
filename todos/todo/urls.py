from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic.simple import direct_to_template

from todos.todo.api import TodoResource

admin.autodiscover()

todo_resource = TodoResource()


urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', direct_to_template, {'template': 'index.html'}),

    (r'^', include(todo_resource.urls)),
)
