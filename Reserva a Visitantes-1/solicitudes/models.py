from django.db import models
from datetime import datetime #tiempo
from django.contrib.auth.models import AbstractBaseUser
# Create your models here.


class TipoUsuario(models.Model):
    """Model definition for TipoUsuario."""
    nombre = models.CharField('Nombre', max_length=50)
    estado = models.BooleanField(default=True)

    class Meta:
        """Meta definition for TipoUsuario."""

        verbose_name = 'TipoUsuario'
        verbose_name_plural = 'TipoUsuarios'

    def __str__(self):
        """Unicode representation of TipoUsuario."""
        return self.nombre


class Cargo(models.Model):
    """Model definition for Cargo."""
    nombre = models.CharField('Nombre', max_length=50)
    estado = models.BooleanField(default=True)

    class Meta:
        """Meta definition for Cargo."""

        verbose_name = 'Cargo'
        verbose_name_plural = 'Cargos'

    def __str__(self):
        """Unicode representation of Cargo."""
        return self.nombre

class Persona(models.Model):
    """Model definition for Persona."""
    nombres = models.CharField('Nombres', max_length=60)
    apellidos = models.CharField('Apellidos', max_length=60)
    cedula = models.CharField('Cedula',max_length=10, unique=True)
    email = models.CharField('Correo',max_length=50, unique=True)
    telefono = models.CharField('Teefono',max_length=10)
    ciudad = models.CharField('Ciudad', max_length=20, blank=True)
    avatar = models.ImageField('Avatar',upload_to='avatar/persona/%Y/%m/%d/', default='avatar/default_avatar.png')

    class Meta:
        """Meta definition for Persona."""
        verbose_name = 'Persona'
        verbose_name_plural = 'Personas'
    def __str__(self):
       return f'{self.nombres} {self.apellidos}'


class Horario(models.Model):
    HorarioInicio = models.TimeField(blank=True)
    HorarioFin = models.TimeField(blank=True)
    estado = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.HorarioInicio} - {self.HorarioFin}'


class Funcionario(models.Model):
    """Model definition for Funcionario."""
    id_persona = models.ForeignKey(Persona, on_delete=models.CASCADE)
    id_cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE)
    horario = models.ManyToManyField(Horario)
    estado = models.BooleanField(default=True)

    class Meta:
        """Meta definition for Funcionario."""
        verbose_name = 'Funcionario'
        verbose_name_plural = 'Funcionarios'

    def __str__(self):
        return self.id_persona.nombres
    


class Visitante(models.Model):
    """Model definition for Visitante."""
    id_persona = models.ForeignKey(Persona, on_delete=models.CASCADE)
    estado = models.BooleanField(default=True)

    class Meta:
        """Meta definition for Visitante."""
        verbose_name = 'Visitante'
        verbose_name_plural = 'Visitantes'

    def __str__(self):
        return f'{self.id_persona.nombres} {self.id_persona.apellidos}'
    


class Usuario(models.Model):
    """Model definition for Usuario."""
    id_persona = models.ForeignKey(Persona, on_delete=models.CASCADE)
    id_tipousuario = models.ForeignKey(TipoUsuario, on_delete=models.CASCADE)
    username = models.CharField('Usuario', max_length=50)
    password = models.CharField(max_length=50)
    estado = models.BooleanField(default=True)
    class Meta:
        """Meta definition for Usuario."""
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        return self.id_persona.nombres



class Solicitud(models.Model):
    """Model definition for Solicitud."""
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('aprobado', 'Aprobado'),
        ('rechazado', 'Rechazado'),
        ('procesado', 'Procesado'),
    ]
    id_visitante = models.ForeignKey(Visitante, on_delete=models.CASCADE)
    id_funcionario = models.ForeignKey(Funcionario, on_delete=models.CASCADE)
    motivo = models.CharField('Motivo', max_length=50)
    fecha = models.DateField(default=datetime.now)
    fecha_reservada = models.DateField(null=True)
    horario = models.CharField( max_length=50)
    codigo_qr = models.CharField('Codigo Qr',max_length=255, unique=True)
    estado_solicitud = models.CharField('Estado', max_length=20, choices=ESTADO_CHOICES, default='pendiente', blank=True)
    estado = models.BooleanField(default=True)

    class Meta:
        """Meta definition for Solicitud."""

        verbose_name = 'Solicitud'
        verbose_name_plural = 'Solicitudes'

    def __str__(self):
        return f'{self.id_visitante.id_persona.nombres}-{self.id}'



class ResgistroVisita(models.Model):
    """Model definition for ResgistroVisita."""
    id_solicitud = models.ForeignKey(Solicitud, on_delete=models.CASCADE)
    fecha_ingreso = models.DateTimeField('Fecha de ingreso', default=datetime.now)
    estado = models.BooleanField(default=True)

    class Meta:
        """Meta definition for ResgistroVisita."""
        verbose_name = 'ResgistroVisita'
        verbose_name_plural = 'ResgistroVisitas'

    def __str__(self):
        return self.id_solicitud.id_visitante.id_persona.nombres
