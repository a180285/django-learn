from django.shortcuts import render

from django.views import generic

# Create your views here.

class IndexView(generic.base.TemplateView):
    template_name = 'p2p/index.html'
