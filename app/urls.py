
from django.urls import path
from .views import *
from django import views
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    
    #Principal
    path('' , iniciovista.as_view() , name= 'Inicio' ),
    
    #Login/Register/Cambio
    
    path('Login/', LoginPagina.as_view(), name = 'Login' ),
    path('logout/', logout_view , name='Logout'),
    path('Register/', RegistroPagina.as_view(), name = 'Register' ),
    path('CambiarPasword/', CambioPassword.as_view(), name = 'CambiarPasword' ),
    path('passwordExitoso/', RegistroPagina.as_view(), name = 'passwordExitoso' ),
    path('EdicionUsuario/', UsuarioEdicion.as_view(), name = 'EdicionUsuario' ),
    
    #Constelaciones
    
    path('constelaciones/', ConstelacionListView.as_view(), name='constelaciones'),
    path('ConstelacionDetalle/<int:pk>/', ConstelacionDetalleView.as_view(), name='ConstelacionDetalle'),
    path('ConstelacionUpdate/<int:pk>/', ConstelacionUpdateView.as_view(), name='ConstelacionUpdate'),
    path('ConstelacionDelete/<int:pk>/', ConstelacionDeleteView.as_view(), name='ConstelacionDelete'),
    path('CreacionConstelacion/', ConstelacionCreacion.as_view(), name='CreacionConstelacion'),

    
   # Profesores
    path('profesores/', ProfesoresListView.as_view(), name='Profesores'),
    path('profesoresDetalle/<int:pk>/', ProfesoresDetalleView.as_view(), name='profesoresDetalle'),
    path('profesoresUpdate/<int:pk>/', profesoresUpdateView.as_view(), name='profesoresUpdate'),
    path('profesoresDelete/<int:pk>/', profesoresDeleteView.as_view(), name='profesoresDelete'),
    path('ProfesorNuevo/', ProfesoresCreacion.as_view(), name='ProfesorNuevo'),
    
    
    #Creacion de ambos
    
    path('CreacionConstelacion/' , ConstelacionCreacion.as_view() , name= 'CreacionConstelacion' ),
    
    
    #Comentario
    
    path('ConstelacionDetalle/<int:pk>/comentario/', ComentarioPagina.as_view(), name='comentario'),





    path('conversaciones/', views.conversaciones, name='conversaciones'),
    path('mensajes/<int:conversacion_id>/', views.mensajes, name='mensajes'),
    path('iniciar-conversacion/<int:usuario_id>/', views.iniciar_conversacion, name='iniciar_conversacion'),
    
    
    path('profesores/' , Profesores , name= 'profesores' ),
    
    
    
    path('informacion/' , informacion , name= 'informacion' ),
    
    
    path('conoceme/' , conoceme , name= 'conoceme' ),
] 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)