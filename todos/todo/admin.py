from django.contrib import admin
from todos.todo.models import Category, Todo


class CategoryAdmin(admin.ModelAdmin):
    pass
admin.site.register(Category, CategoryAdmin)


class TodoAdmin(admin.ModelAdmin):
    pass
admin.site.register(Todo, TodoAdmin)
