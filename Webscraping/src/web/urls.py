
from django.contrib import admin
from django.urls import path,include
from Recomendacion.views import index,registro,RegistrarUsuario,login,Loguearse,deslog,userPanel,AdminPanel,SistemaRecomendacion,MostrarUSuarios,GestionTelevisores,ListarTelevisores,EstadisticasTelevisores

urlpatterns = [    
    path('', index, name='index'),    
    path('registro/',registro,name='registro'),
    path('RegistrarUsuario/',RegistrarUsuario,name='RegistrarUsuario'),
    path('login/',login,name='login'),
    path('logeo/',Loguearse,name='Loguearse'),
    path('deslog/',deslog,name='deslog'),
    path('userPanel/',userPanel,name='userPanel'),    
    path('AdminPanel/',AdminPanel,name='AdminPanel'),
    path('AdminPanel/GestionTelevisores',GestionTelevisores,name='GestionTelevisores'),
    path('AdminPanel/GestionTelevisores/listarTelevisores',ListarTelevisores,name='ListarTelevisores'),
    path('AdminPanel/GestionTelevisores/EstadisticasTelevisores',EstadisticasTelevisores,name='EstadisticasTelevisores'),
    path('AdminPanel/SistemaRecomendacion',SistemaRecomendacion,name='SistemaRecomendacion'),
    path('AdminPanel/MostrarUsuarios',MostrarUSuarios,name='MostrarUSuarios'),
]
