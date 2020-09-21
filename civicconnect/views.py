from django.utils import timezone
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

# from .models import Choice, Question, Comment


class IndexView(generic.ListView):
    template_name = 'civicconnect/index.html'
    def get_queryset(self):
        """
        Just a blank one for now...
        """
        return "1"
