from django.http import HttpResponsePermanentRedirect
from django.urls import reverse


def home(request):
    return HttpResponsePermanentRedirect(reverse('repos:list'))
