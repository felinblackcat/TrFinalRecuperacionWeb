from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets

# Create your views here.
def index (request):
    return render(request,'index.html')