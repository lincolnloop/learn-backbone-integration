from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView

from todos.todo.views import CategoryList, CategoryDetail, TodoList, TodoDetail

admin.autodiscover()


urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),

    url(r'^todos/$', TodoList.as_view(), name='todo-list'),
    url(r'^todos/(?P<pk>\d+)/$', TodoDetail.as_view(), name='todo-detail'),
    url(r'^categories/$', CategoryList.as_view(), name='category-list'),
    url(r'^categories/(?P<pk>\d+)/$', CategoryDetail.as_view(),
        name='category-detail'),

    # For the browseable API
    url(r'^api-auth/', include('rest_framework.urls',
        namespace='rest_framework')),

    url(r'^$', TemplateView.as_view(template_name="index.html")),
)
