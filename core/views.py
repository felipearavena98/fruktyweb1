from django.shortcuts import render

# Create your views here.
from django.views.generic.base import TemplateView


class HomePageView(TemplateView):
    template_name = "core/home.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'title':"Mi Super Web Playground"})

class SamplePageView(TemplateView):
    template_name = "core/sample.html"

    