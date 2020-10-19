from django.contrib import admin

from .models import Topic, Template, Comment
# Register your models here.

admin.site.register(Topic)
admin.site.register(Template)
admin.site.register(Comment)