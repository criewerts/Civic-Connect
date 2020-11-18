from django.contrib import admin

from .models import Topic, Template, Representative

models = [Topic, Template, Representative]
admin.site.register(models)