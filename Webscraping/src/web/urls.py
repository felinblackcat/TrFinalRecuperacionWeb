
from django.contrib import admin
from django.urls import path,include
from Recomendacion.views import index,registro,RegistrarUsuario,login,Loguearse,deslog,userPanel,AdminPanel,SistemaRecomendacion,MostrarUSuarios,GestionTelevisores,ListarTelevisores,EstadisticasTelevisores,BuscarTelevisor,MostrarTelevisores,ModalTelevisores,MostarCalificaciones,MostrarRecomendaciones,MostrarPresicion,GuardarCalificacion,VerRecomendaciones
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [    
    path('', index, name='index'),    
    path('registro/',registro,name='registro'),
    path('RegistrarUsuario/',RegistrarUsuario,name='RegistrarUsuario'),
    path('login/',login,name='login'),
    path('logeo/',Loguearse,name='Loguearse'),
    path('guardarcal/',GuardarCalificacion,name='GuardarCalificacion'),
    path('deslog/',deslog,name='deslog'),
    path('userPanel/',userPanel,name='userPanel'),    
    path('AdminPanel/',AdminPanel,name='AdminPanel'),
    path('userPanel/MostrarTelevisores',MostrarTelevisores,name='MostrarTelevisores'),
    path('userPanel/VerRecomendaciones',VerRecomendaciones,name='VerRecomendaciones'),
    path('userPanel/MostrarTelevisores/ModalTelevisores',ModalTelevisores,name='ModalTelevisores'),
    path('AdminPanel/GestionTelevisores',GestionTelevisores,name='GestionTelevisores'),
    path('AdminPanel/GestionTelevisores/listarTelevisores',ListarTelevisores,name='ListarTelevisores'),
    path('AdminPanel/GestionTelevisores/EstadisticasTelevisores',EstadisticasTelevisores,name='EstadisticasTelevisores'),
    path('AdminPanel/SistemaRecomendacion',SistemaRecomendacion,name='SistemaRecomendacion'),
    path('AdminPanel/MostrarUsuarios',MostrarUSuarios,name='MostrarUSuarios'),
    path('AdminPanel/ResultadoBusqueda',BuscarTelevisor,name='BuscarTelevisor'),
    path('AdminPanel/SistemaRecomendacion/Calificaciones',MostarCalificaciones,name='MostarCalificaciones'),
    path('AdminPanel/SistemaRecomendacion/Recomendaciones',MostrarRecomendaciones,name='MostrarRecomendaciones'),
    path('AdminPanel/SistemaRecomendacion/Presicion',MostrarPresicion,name='MostrarPresicion'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
