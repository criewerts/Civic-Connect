from django.contrib import admin

from .models import Topic, Template, Comment, Representative

models = [Topic, Template, Comment, Representative]
admin.site.register(models)