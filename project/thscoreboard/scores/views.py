from django.shortcuts import render
from django.views.decorators import http as http_decorators
from django import http

@http_decorators.require_safe
def index(request):
    return render(request, 'scores/index.html')
