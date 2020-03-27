from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from src.Bot.Bot import scraper
# Create your views here.
@csrf_exempt
def index (request):
    return render(request,'index.html')

@csrf_exempt
def runspider(request):
     print("Respuesta",request)
     #scraper.configure_logging()
     #scraper.get_project_settings()
     
     
     #scraper.startScan()
     #scraper.reactor.run()
     context = {
                'resultado':'ArañaEjecucion',
            } 
     return render(request,'alltelevisores.html',context)
 
    