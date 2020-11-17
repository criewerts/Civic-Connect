from django.utils import timezone
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.forms import ModelForm
from users.models import CustomUser
import requests, json
from datetime import datetime
from civic14.settings import API_KEY
from civicconnect.models import Topic, Template, Representative
from civicconnect.forms import RepresentativeForm
from django.contrib import messages

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
        ).order_by('-pub_date')

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
        context = {'topics': Topic.objects.filter(), 'affiliations': Template._meta.get_field('affiliation').choices}
        return render(request, 'civicconnect/template_create.html', context)

    def post(self, request, *args, **kwargs):
        template = Template.objects.create(
            title=request.POST['title'],
            author=CustomUser.objects.get(email=request.user.email),
            topic=Topic.objects.get(pk=request.POST['topic']),
            body=request.POST['body'],
            affiliation=request.POST['affiliation'],
            pub_date=datetime.now()
        )
        messages.success(request, "<strong>Success!</strong> Your template has been created.")
        return HttpResponseRedirect(reverse('civicconnect:template_detail', args=[template.id]))
        # return render(request, 'civicconnect/template_create.html', {'form': form})

class TemplateUpdateView(generic.DetailView):
    model = Template
    template_name = 'civicconnect/template_create.html'
    
    def get(self, request, *args, **kwargs):
        context = {'topics': Topic.objects.filter(), 'affiliations': Template._meta.get_field('affiliation').choices, "template": Template.objects.get(pk=self.kwargs['pk'])}
        return render(request, 'civicconnect/template_create.html', context)

    def post(self, request, *args, **kwargs):
        template = Template.objects.get(pk=self.kwargs['pk'])
        template.title=request.POST['title']
        template.topic=Topic.objects.get(pk=request.POST['topic'])
        template.body=request.POST['body']
        template.affiliation=request.POST['affiliation']
        template.save()
        messages.success(request, "Successfully edited <strong>" + request.POST['title'] + "</strong>.")
        return HttpResponseRedirect(reverse('civicconnect:template_detail', args=[template.id]))
        # return render(request, 'civicconnect/template_create.html', {'form': form})

class TemplateGenerateView(generic.DetailView):
    template_name = 'civicconnect/template_generate.html'

    def post(self, request, *args, **kwargs):
        # template = get_object_or_404(Template, pk=request.POST['template'])
        raw_template = Template.objects.get(pk=request.POST['template']).body
        raw_template = raw_template.replace("${official}", request.POST['official'])
        raw_template = raw_template.replace("${me}", request.POST['me'])
        raw_template = raw_template.replace("\n", "<br>")
        payload = {
            'template': Template.objects.get(pk=request.POST['template']),
            'official': {'name': request.POST['official'], 'email': request.POST['email']},
            'generated_template': raw_template
        }
        messages.success(request, "<strong>Success!</strong> Please find your generated email below.")
        return render(request, self.template_name, payload)

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
            messages.success(request, "<strong>Success!</strong> Your topic has been created.")
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
                args = {'officials': data['officials'], 'original': data['normalizedInput'], 'offices': data['offices'], 'templates': Template.objects.filter()}
            else:
                args = {'nothing': 0}

            return render(request, self.success_url, args)

        form = RepresentativeForm()
        return render(request, self.template_name, {'form': form})

def get_user_profile(request, email):
    user = CustomUser.objects.get(email=email)
    return render(request, 'civicconnect/profile.html', {"profile_user":user})

def update_user_profile(request, email):
    user = CustomUser.objects.get(email=request.user.email)
    user.address1 = request.POST['address1']
    user.zip_code = request.POST['zip_code']
    user.city = request.POST['city']
    user.state_cd = request.POST['state_cd']
    user.save()
    messages.success(request, 'Successfully updated your profile information.')
    return render(request, 'civicconnect/profile.html', {"profile_user":user})

def like(request, pk):
    user = CustomUser.objects.get(email=request.user.email)
    if "topics" in request.path:
        fav = Topic.objects.get(pk=pk)
        user.favorites_topic.add(fav)
        messages.success(request, 'Added to your liked topics.')
        return HttpResponseRedirect(reverse('civicconnect:topic_detail', args=[pk]))
    else: # templates
        fav = Template.objects.get(pk=pk)
        user = CustomUser.objects.get(email=request.user.email)
        user.favorites.add(fav)
        messages.success(request, 'Added to your liked templates.')
        return HttpResponseRedirect(reverse('civicconnect:template_detail', args=[pk]))

def unlike(request, pk):
    user = CustomUser.objects.get(email=request.user.email)
    if "topics" in request.path:
        fav = Topic.objects.get(pk=pk)
        user.favorites_topic.remove(fav)
        messages.success(request, 'Removed from your liked topics.')
        return HttpResponseRedirect(reverse('civicconnect:topic_detail', args=[pk]))
    else: # templates
        fav = Template.objects.get(pk=pk)
        user = CustomUser.objects.get(email=request.user.email)
        user.favorites.remove(fav)
        messages.success(request, 'Removed from your liked templates.')
        return HttpResponseRedirect(reverse('civicconnect:template_detail', args=[pk]))