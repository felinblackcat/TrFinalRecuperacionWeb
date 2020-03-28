
from django.contrib import admin
from django.urls import path,include
from Recomendacion.views import index,registro,RegistrarUsuario,login,Loguearse,deslog

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),    
    path('registro/',registro,name='registro'),
    path('RegistrarUsuario/',RegistrarUsuario,name='RegistrarUsuario'),
    path('login/',login,name='login'),
    path('logeo/',Loguearse,name='Loguearse'),
    path('deslog/',deslog,name='deslog')
]
