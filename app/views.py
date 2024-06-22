from django.views.generic import TemplateView, ListView, DetailView, UpdateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView 
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from .forms import *
from django.contrib.auth import logout
from .models import *



class iniciovista(TemplateView):
    template_name = "Inicio.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profesores'] = Profesores.objects.all()
        context['constelaciones'] = Constelaciones.objects.all()
        
        return context
    


#Todo relacionado al login/register

class LoginPagina(LoginView):
    template_name = 'login.html'
    fields = '__all__'
    redirect_autheticated_user = True
    success_url = reverse_lazy('Inicio')

    def get_success_url(self):
        return reverse_lazy('Inicio')

class RegistroPagina(FormView):
    template_name = 'registro.html'
    form_class = FormularioRegistroUsuario
    redirect_autheticated_user = True
    success_url = reverse_lazy('Inicio')

    def form_valid(self, form):
        user = form.save()
        if user:
            login(self.request, user)
        return super(RegistroPagina, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('Inicio')
        return super(RegistroPagina, self).get(*args, **kwargs)

class UsuarioEdicion(UpdateView):
    form_class = FormularioEdicion
    template_name= 'edicionPerfil.html'
    success_url = reverse_lazy('Inicio')

    def get_object(self):
        return self.request.user

class CambioPassword(PasswordChangeView):
    form_class = FormularioCambioPassword
    template_name = 'passwordCambio.html'
    success_url = reverse_lazy('passwordExitoso')
    
def logout_view(req):
    logout(req)
    return redirect('Inicio')    
    
def password_exitoso(request):
    return render(request, 'passwordExitoso.html', {})


#Constelaciones


class ConstelacionListView(LoginRequiredMixin, ListView):
    model = Constelaciones
    context_object_name = 'constelaciones'
    template_name = 'constelaciones_Vista.html'
    queryset = Constelaciones.objects.all()
    login_url = '/Login/'

class ConstelacionDetalleView(LoginRequiredMixin, DetailView):
    model = Constelaciones
    context_object_name = 'constelacion'
    template_name = 'ConstelacionDetalle.html'

class ConstelacionUpdateView(LoginRequiredMixin, UpdateView):
    model = Constelaciones
    form_class = CambioConstelacion
    success_url = reverse_lazy('constelaciones')
    context_object_name = 'constelacion'
    template_name = 'ConstelacionEdicion.html'

class ConstelacionDeleteView(LoginRequiredMixin, DeleteView):
    model = Constelaciones
    success_url = reverse_lazy('constelaciones')
    context_object_name = 'constelacion'
    template_name = 'ConstelacionBorrado.html'



#Profesores

class ProfesoresListView(LoginRequiredMixin, ListView):
    model = Profesores
    context_object_name = 'profesores'
    template_name = 'Profesores_Vista.html'
    queryset = Profesores.objects.all()
    login_url = '/Login/'

    
class ProfesoresDetalleView(LoginRequiredMixin, DetailView):
    model = Profesores
    context_object_name = 'profesor'
    template_name = 'ProfesorDetalle.html'


class profesoresUpdateView(LoginRequiredMixin, UpdateView):
    model = Profesores
    form_class = CambioProfesor
    success_url = reverse_lazy('profesores')
    context_object_name = 'profesor'
    template_name = 'ProfesorEdicion.html'

class profesoresDeleteView(LoginRequiredMixin, DeleteView):
    model = Profesores
    success_url = reverse_lazy('profesores')
    context_object_name = 'profesor'
    template_name = 'ProfesorBorrado.html'
    
    
#Creacion Constelaciones


class ConstelacionCreacion(LoginRequiredMixin, CreateView):
    model = Constelaciones
    form_class = FormularioNuevaConstelacion
    success_url = reverse_lazy('Inicio')
    template_name = 'ConstelacionNueva.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(ConstelacionCreacion, self).form_valid(form)    


#Creacion Profesores

class ProfesoresCreacion(LoginRequiredMixin, CreateView):
    model = Profesores
    form_class = FormularioNuevoProfesor
    success_url = reverse_lazy('Inicio')
    template_name = 'ProfesorNuevo.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(ProfesoresCreacion, self).form_valid(form)    

# Defino la creacion de los comentarios

class ComentarioPagina(LoginRequiredMixin, CreateView):
    model = Comentario
    form_class = FormularioComentario
    template_name = 'loscomentarios.html'
    success_url = reverse_lazy('Inicio')

    def form_valid(self, form):
        form.instance.comentario_id = self.kwargs['pk']
        return super(ComentarioPagina, self).form_valid(form)







def informacion(req):
    
    return render(req , 'informacion_Vista.html', {} )



def conoceme(req):
    
    return render(req , 'conoceme_Vista.html', {} )

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Conversacion, Mensaje
from .forms import MensajeForm


@login_required
def conversaciones(request):
    # Obtener conversaciones del usuario actual
    conversaciones = Conversacion.objects.filter(Q(usuario1=request.user) | Q(usuario2=request.user)).order_by('-fecha_inicio')

    # Obtener todos los usuarios excepto el usuario actual
    usuarios = User.objects.exclude(id=request.user.id)

    context = {
        'conversaciones': conversaciones,
        'usuarios': usuarios,  # Añadir usuarios al contexto
    }
    return render(request, 'conversaciones.html', context)

@login_required
def mensajes(request, conversacion_id):
    conversacion = Conversacion.objects.get(id=conversacion_id)
    mensajes = conversacion.mensajes.order_by('fecha_envio')
    form = MensajeForm()

    if request.method == 'POST':
        form = MensajeForm(request.POST)
        if form.is_valid():
            mensaje = form.save(commit=False)
            mensaje.emisor = request.user
            mensaje.receptor = conversacion.usuario1 if request.user != conversacion.usuario1 else conversacion.usuario2
            mensaje.conversacion = conversacion
            mensaje.save()
            return redirect('mensajes', conversacion_id=conversacion.id)

    context = {
        'conversacion': conversacion,
        'mensajes': mensajes,
        'form': form,
    }
    return render(request, 'mensajes.html', context)

from django.shortcuts import get_object_or_404

from django.contrib.auth.models import User

@login_required
def iniciar_conversacion(request, usuario_id):
    # Obtener el usuario destinatario
    destinatario = get_object_or_404(User, id=usuario_id)

    # Crear o obtener la conversación entre el usuario actual y el destinatario
    conversacion = Conversacion.objects.get_or_create_conversation(request.user, destinatario)
    

    # Redirigir a la vista de mensajes de esta conversación
    return redirect('mensajes', conversacion_id=conversacion.id)