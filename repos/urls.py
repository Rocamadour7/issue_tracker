from django.urls import path

from .views import RepoList

app_name = 'repos'

urlpatterns = [
    path('', RepoList.as_view(), name='list'),
]
