import datetime
from django.conf import settings
from django.db import models
from django.utils import timezone
from users.models import CustomUser


class Topic(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
    def __str__(self):
        return self.title

class Template(models.Model):
    AFFILIATIONS = [
        (1, 'Bipartisan'),
        (2, 'Left-Wing'),
        (3, 'Right-Wing'),
        (4, 'Moderate'),
    ]
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    body = models.TextField()
    affiliation = models.IntegerField(choices=AFFILIATIONS, default=1)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return self.title
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'


class Comment(models.Model):
    template = models.ForeignKey(Template, on_delete=models.CASCADE)
    message = models.TextField(default="")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
    date = models.DateTimeField(default=datetime.datetime.now())
    def __str__(self):
        return self.message


class Representative(models.Model):
    name = models.CharField(max_length=200, default='')
    party = models.CharField(max_length=100, default='')
    phone = models.CharField(max_length=20, default='')
    address = models.TextField(default='')
    user = models.ForeignKey(CustomUser, null=True,  on_delete=models.SET_NULL)

    def __str__(self):
        return self.name
