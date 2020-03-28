from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
import os
from src.Bot.Bot import scraper
import threading
# Create your views here.
import json


def ejecutar_spyders():
    scraper.startScan()
    scraper.reactor.run()
    data = {}
    data["Estado"]="false"
    with open('data.json', 'w') as file:json.dump(data, file, indent=4)

@csrf_exempt
def index (request):
    return render(request,'index.html')

@csrf_exempt
def runspider(request):
    hilo  = threading.Thread(target=ejecutar_spyders)
    if(os.path.isfile('data.json')):
        
        with open('data.json') as file:data = json.load(file)
        if(data['Estado']=="true"):
            
            context = {
                    'mensaje':'Error la araña ya se esta ejecutando intendalo mas tarde.',
                } 
            return render(request,'alltelevisores.html',context)
        elif(data['Estado']=="false"):
            
            data = {}
            data['Estado']="true"
            with open('data.json', 'w') as file:json.dump(data, file, indent=4)
            hilo.start()
            context = {
                'mensaje':'Inicio del proceso de scraping...',
                }   
            return render(request,'alltelevisores.html',context)
        
        
        
    else:
        print("Entro")
        data = {}
        data['Estado']="true"
        with open('data.json', 'w') as file:json.dump(data, file, indent=4)
        hilo.start()
        context = {
                'mensaje':'Inicio del proceso de scraping...',
            }  
     
     
        return render(request,'alltelevisores.html',context)
         
         
        
         
     
         
 
 