from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic.simple import direct_to_template

from todos.todo.views import CategoryView, TodoView

admin.autodiscover()


urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),

    url(r'^categories(?:/(?P<pk>\d+))?/$', CategoryView.as_view(),
        name='categories'),
    url(r'^todos(?:/(?P<pk>\d+))?/$', TodoView.as_view(), name='todos'),

    url(r'^$', direct_to_template, {'template': 'index.html'}),
)
