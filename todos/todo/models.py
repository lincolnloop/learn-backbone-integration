from django.db import models


class Todo(models.Model):
    title = models.CharField(max_length=200)
    order = models.IntegerField(null=True, blank=True)
    done = models.BooleanField(default=False)
    owner = models.ForeignKey('auth.User')

    def __unicode__(self):
        return self.title
