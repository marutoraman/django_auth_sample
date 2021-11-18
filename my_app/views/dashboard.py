from django.shortcuts import render
from django.http.response import HttpResponse
from django.views.generic import TemplateView

app_name = "my_app"

class DashboardView(TemplateView):
    template_name = f"{app_name}/dashboard.html"