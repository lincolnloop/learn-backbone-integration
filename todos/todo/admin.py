from django.contrib import admin
from todos.todo.models import Todo


class TodoAdmin(admin.ModelAdmin):
    pass


admin.site.register(Todo, TodoAdmin)
