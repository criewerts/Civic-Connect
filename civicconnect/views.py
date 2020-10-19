from django.utils import timezone
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.forms import ModelForm

from .models import Topic, Template


class IndexView(generic.ListView):
    template_name = 'civicconnect/index.html'
    def get_queryset(self):
        """
        Just a blank one for now...
        """
        return "1"

class TemplateIndexView(generic.ListView):
    template_name = 'civicconnect/template_index.html'
    context_object_name = 'template_list'

    def get_queryset(self):
        return Template.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]

class TemplateDetailView(generic.DetailView):
    model = Template
    template_name = 'civicconnect/template_detail.html'
    def get_queryset(self):
        return Template.objects.filter(pub_date__lte=timezone.now())

class TemplateCreateForm(ModelForm):
        class Meta:
            model = Template
            fields = '__all__'

class TemplateCreateView(generic.CreateView):
    # model = Template
    template_name = 'civicconnect/template_create.html'
    
    def get(self, request, *args, **kwargs):
        context = {'form': TemplateCreateForm()}
        return render(request, 'civicconnect/template_create.html', context)

    def post(self, request, *args, **kwargs):
        form = TemplateCreateForm(request.POST)
        if form.is_valid():
            template = form.save()
            template.save()
            return HttpResponseRedirect(reverse('civicconnect:template_detail', args=[template.id]))
        return render(request, 'civicconnect/template_create.html', {'form': form})

class TopicIndexView(generic.ListView):
    template_name = 'civicconnect/topic_index.html'
    context_object_name = 'topic_list'

    def get_queryset(self):
        return Topic.objects.filter()

class TopicDetailView(generic.DetailView):
    model = Topic
    template_name = 'civicconnect/topic_detail.html'
    def get_queryset(self):
        return Topic.objects.filter()