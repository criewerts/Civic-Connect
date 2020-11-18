from django.conf.urls import include, url
from django.urls import path

from . import views

app_name = 'civicconnect'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('templates/', views.TemplateIndexView.as_view(), name='template_index'),
    path('templates/create/', views.TemplateCreateView.as_view(), name='template_create'),
    path('templates/<int:pk>/', views.TemplateDetailView.as_view(), name='template_detail'),
    path('templates/<int:pk>/edit', views.TemplateUpdateView.as_view(), name='template_update'),
    path('templates/<int:pk>/autoapprove', views.auto_approve, name='auto_approve'),
    path('topics/', views.TopicIndexView.as_view(), name='topic_index'),
    path('topics/create/', views.TopicCreateView.as_view(), name='topic_create'),
    path('topics/<int:pk>/', views.TopicDetailView.as_view(), name='topic_detail'),
    path('topic/<int:pk>/edit', views.TopicUpdateView.as_view(), name='topic_update'),
    path('representatives/', views.RepresentativeView.as_view(), name='repindex_view'),
    path('generate/', views.TemplateGenerateView.as_view(), name='generate'),
    url(r'profile/(?P<email>.+)/update$', views.update_user_profile, name="update_profile"),
    url(r'profile/(?P<email>.+)$', views.get_user_profile, name="profile"),
    url(r'templates/(?P<pk>[0-9]+)/like', views.like, name='like'),
    url(r'templates/(?P<pk>[0-9]+)/unlike', views.unlike, name='unlike'),
    url(r'topics/(?P<pk>[0-9]+)/like', views.like, name='like_topic'),
    url(r'topics/(?P<pk>[0-9]+)/unlike', views.unlike, name='unlike_topic')
]
