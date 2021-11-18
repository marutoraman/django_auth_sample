from django.shortcuts import render
from django.http.response import HttpResponse
from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = "index.html"
    
    
class LoginRequiredView(TemplateView):
    template_name = "login_required.html"