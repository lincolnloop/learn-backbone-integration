from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic.simple import direct_to_template

from todos.todo.views import TodoView

admin.autodiscover()


urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),

    url(r'^todos(?:/(?P<pk>\d+))?/$', TodoView.as_view()),

    url(r'^$', direct_to_template, {'template': 'index.html'}),
)
