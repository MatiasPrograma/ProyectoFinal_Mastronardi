from django.db import models
from django.contrib.auth.models import User


class Constelaciones(models.Model):
    constelaciondisponibles = (
        ('Relación padres-hijos', 'relación padres-hijos'),
        ('Pareja', 'pareja'),
        ('Excluidos', 'excluidos'),
        ('Divorcios o separaciones', 'divorcios o separaciones'),
        ('Trabajo', 'trabajo'),
        ('Guerras', 'guerras'),
        ('Muertes tempranas', 'muertes tempranas'),
        ('otros', 'Otros'),
    )

    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    titulo = models.CharField(max_length=200)
    constelacion = models.CharField(max_length=40, choices=constelaciondisponibles, default='Pareja')
    profesor = models.CharField(max_length=40)
    descripcion = models.TextField(null=True, blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    fechaPublicacion = models.DateTimeField(auto_now_add=True)
    telefonoContacto = models.IntegerField()
    emailContacto = models.EmailField()
    imagendeconstelacion = models.ImageField(null=True, blank=True, upload_to="imagenes/")

    class Meta:
        ordering = ['usuario', '-fechaPublicacion']

    def __str__(self):
        return self.titulo
    
    
class Profesores(models.Model):

    constelaciondisponibles =(
        ('Relación padres-hijos' , 'relación padres-hijos' ) ,
        ('Pareja' , 'pareja'),
        ('Excluidos' , 'excluidos'),
        ('Divorcios o separaciones' , 'divorcios o separaciones' ),
        ('Trabajo','trabajo'),
        ('Guerras' , 'guerras'),
        ('Muertes tempranas', 'muertes tempranas'),
        ('otros' , 'Otros'),
        
    )
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    Profesor = models.CharField(max_length=200)
    constelacionnesDadas = models.CharField(max_length=40, choices=constelaciondisponibles, default='Ninguna')
    descripcion = models.TextField(null=True, blank=True)
    fechaPublicacion = models.DateTimeField(auto_now_add=True)
    telefonoContacto = models.IntegerField()
    emailContacto = models.EmailField()
    imagendeProfesor = models.ImageField(null=True, blank=True, upload_to="media/")
    
    

    class Meta:
        ordering = ['usuario', '-fechaPublicacion']


    def __str__(self):
        return self.Profesor


class Comentario(models.Model):
    comentario = models.ForeignKey(Constelaciones, related_name='comentarios', on_delete=models.CASCADE, null=True)
    nombre = models.CharField(max_length=40)
    mensaje = models.TextField(null=True, blank=True)
    fechaComentario = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fechaComentario']

    def __str__(self):
        return '%s - %s' % (self.nombre, self.comentario)
    
    

class Avatar(models.Model):
    
    user =models.OneToOneField(User, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='avatares' , null=True , blank=True)
    
    def __str__(self):
        
        return f"{self.user} - {self.imagen}"
    
    
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q

class ConversacionManager(models.Manager):
    def get_or_create_conversation(self, usuario1, usuario2):
        q1 = Q(usuario1=usuario1, usuario2=usuario2)
        q2 = Q(usuario1=usuario2, usuario2=usuario1)
        conversacion_existente = Conversacion.objects.filter(q1 | q2).first()

        if conversacion_existente:
            return conversacion_existente
        else:
            nueva_conversacion = Conversacion(usuario1=usuario1, usuario2=usuario2)
            nueva_conversacion.save()
            return nueva_conversacion

class Conversacion(models.Model):
    usuario1 = models.ForeignKey(User, related_name='conversaciones_iniciadas', on_delete=models.CASCADE)
    usuario2 = models.ForeignKey(User, related_name='conversaciones_recibidas', on_delete=models.CASCADE)
    fecha_inicio = models.DateTimeField(auto_now_add=True)

    objects = ConversacionManager()  # Asigna el manager al modelo

    class Meta:
        unique_together = [['usuario1', 'usuario2']]
        ordering = ['-fecha_inicio']

    def __str__(self):
        return f'Conversación entre {self.usuario1.username} y {self.usuario2.username}'


class Mensaje(models.Model):
    conversacion = models.ForeignKey(Conversacion, related_name='mensajes', on_delete=models.CASCADE)
    emisor = models.ForeignKey(User, related_name='mensajes_enviados', on_delete=models.CASCADE)
    receptor = models.ForeignKey(User, related_name='mensajes_recibidos', on_delete=models.CASCADE)
    contenido = models.TextField()
    fecha_envio = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['fecha_envio']

    def __str__(self):
        return f'Mensaje de {self.emisor.username} a {self.receptor.username}'

    def save(self, *args, **kwargs):
        self.conversacion = Conversacion.objects.get_or_create_conversation(self.emisor, self.receptor)
        super().save(*args, **kwargs)


