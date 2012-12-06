from django.db import models


class Category(models.Model):
    title = models.CharField(max_length=300)

    class Meta:
        verbose_name_plural = 'categories'

    def __unicode__(self):
        return self.title


class Todo(models.Model):
    title = models.CharField(max_length=300)
    order = models.IntegerField(null=True, blank=True)
    done = models.BooleanField(default=False)
    owner = models.ForeignKey('auth.User')
    category = models.ForeignKey(Category, null=True, blank=True)

    def __unicode__(self):
        return self.title
