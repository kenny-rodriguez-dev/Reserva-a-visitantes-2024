from django.contrib import admin
from .models import TipoUsuario, Cargo, Persona, Funcionario, Visitante, Usuario, Horario, Solicitud, ResgistroVisita
# Register your models here.

class TipoUsuarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre','estado')

class CargoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'estado')

class PersonaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombres','apellidos', 'cedula','email','telefono','ciudad','avatar')

class FuncionarioAdmin(admin.ModelAdmin):
    list_display = ('id','estado')

class VisitanteAdmin(admin.ModelAdmin):
    list_display = ('id', 'estado')

class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('id','username','password','estado' )

class HorarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'HorarioInicio', 'HorarioFin', 'estado')

class SolicitudAdmin(admin.ModelAdmin):
    list_display = ('id', 'id_funcionario', 'motivo', 'fecha', 'fecha_reservada','horario','codigo_qr','estado','estado_solicitud')

class ResgistroVisitaAdmin(admin.ModelAdmin):
    list_display = ('id', 'fecha_ingreso','estado')



admin.site.register(TipoUsuario, TipoUsuarioAdmin)
admin.site.register(Cargo, CargoAdmin)
admin.site.register(Persona, PersonaAdmin)
admin.site.register(Funcionario, FuncionarioAdmin)
admin.site.register(Visitante, VisitanteAdmin)
admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Horario, HorarioAdmin)
admin.site.register(Solicitud, SolicitudAdmin)
admin.site.register(ResgistroVisita, ResgistroVisitaAdmin)

