from django.utils import timezone
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.forms import ModelForm
import requests, json

from civic14.settings import API_KEY
from .models import Topic, Template, Representative
from civicconnect.forms import RepresentativeForm


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

class TopicCreateForm(ModelForm):
        class Meta:
            model = Topic
            fields = '__all__'

class TopicCreateView(generic.CreateView):
    # model = Template
    template_name = 'civicconnect/topic_create.html'
    
    def get(self, request, *args, **kwargs):
        context = {'form': TopicCreateForm()}
        return render(request, 'civicconnect/topic_create.html', context)

    def post(self, request, *args, **kwargs):
        form = TopicCreateForm(request.POST)
        if form.is_valid():
            topic = form.save()
            topic.save()
            return HttpResponseRedirect(reverse('civicconnect:topic_detail', args=[topic.id]))
        return render(request, 'civicconnect/topic_create.html', {'form': form})

class RepresentativeView(generic.DetailView):
    template_name = 'civicconnect/my_reps_index.html'
    success_url = 'civicconnect/my_reps_detail.html'

    def get(self, request):
        form = RepresentativeForm(request.GET)
        if form.is_valid():
            text = form.cleaned_data['address']
            url = 'https://civicinfo.googleapis.com/civicinfo/v2/representatives?address=' + text + '&includeOffices=true&roles=legislatorUpperBody&roles=legislatorLowerBody&key=' + API_KEY
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                for official in data['officials']:
                    match = False
                    rep = Representative(name=official['name'], party=official['party'], phone=official['phones'], address=official['address'])
                    for person in Representative.objects.all():
                        if rep.name == person.name:
                            match = True
                    if not match:
                        rep.save()
                args = {'officials': data['officials']}
            else:
                args = {'nothing': 0}

            return render(request, self.success_url, args)

        form = RepresentativeForm()
        return render(request, self.template_name, {'form': form})
