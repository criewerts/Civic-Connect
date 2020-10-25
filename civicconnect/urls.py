from django.urls import path

from . import views

app_name = 'civicconnect'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('templates/', views.TemplateIndexView.as_view(), name='template_index'),
    path('templates/create/', views.TemplateCreateView.as_view(), name='template_create'),
    path('templates/<int:pk>/', views.TemplateDetailView.as_view(), name='template_detail'),
    path('topics/', views.TopicIndexView.as_view(), name='topic_index'),
    path('topics/create/', views.TopicCreateView.as_view(), name='topic_create'),
    path('topics/<int:pk>/', views.TopicDetailView.as_view(), name='topic_detail'),
    path('myreps/', views.RepresentativeView.as_view(), name='repindex_view'),
]
