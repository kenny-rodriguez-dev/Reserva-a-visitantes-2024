from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.views import LoginView,LogoutView,TemplateView
import Visitas.settings as setting
from datetime import datetime
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User,Group

import re
import hashlib
import random
from django.db.models import Q

from django.template.loader import render_to_string
# Mensajes
from django.contrib import messages

from solicitudes.funciones import generar_codigo_qr, enviarCorreo, enviarCorreo2
#Creacion de las funciones para permisos para los roles
def is_funcionario_or_superuser(user):
    return user.groups.filter(name='FUNCIONARIO').exists() or user.is_superuser

def is_funcionario_or_superuser_or_guardia(user):
    return user.groups.filter(name='FUNCIONARIO').exists() or user.groups.filter(name='GUARDIA').exists() or user.is_superuser

def is_visitante_or_superuser(user):
    return user.groups.filter(name='VISITANTE').exists() or user.is_superuser

def is_guardia_or_superuser(user):
    return user.groups.filter(name='GUARDIA').exists() or user.is_superuser

def is_superuser(user):
    return user.is_superuser

# Create your views here.
class LoginFormView(LoginView):
    template_name ='login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(setting.LOGIN_REDIRECT_URL)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs) :
        context=super().get_context_data(**kwargs)
        context['title']="Iniciar Secion"
        return context
    
class adminInicioView(TemplateView):
   
    template_name = 'inicio.html'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     user_groups = self.request.user.groups.values_list('name', flat=True)
    #     context['user_groups'] = user_groups
    #     return context

    # def get(self, request, *args, **kwargs):
    #     user_groups = self.request.user.groups.values_list('name', flat=True)

    #     if 'FUNCIONARIO' in user_groups:
    #         # Renderizar la pantalla de inicio para usuarios del grupo FUNCIONARIO
    #         return render(request, 'inicio.html')
    #     elif 'GUARDIA' in user_groups:
    #         # Renderizar la pantalla de inicio para usuarios del grupo GUARDIA
    #         return render(request, 'inicio.html')
    #     elif 'VISITANTE' in user_groups:
    #         # Renderizar la pantalla de inicio para usuarios del grupo GUARDIA
    #         return render(request, 'inicio.html')
    #     else:
    #         return redirect('/adminFuncionarios')
    #         # Manejar otros casos, como usuarios con grupos desconocidos
    #         return super().get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        listaFuncionarios = Funcionario.objects.filter(estado=True ).order_by('id')
        listaVisitantes = Visitante.objects.all().order_by('id')
        listaUsuarios = Usuario.objects.all().order_by('id')
        context['listaFuncionarios'] = listaFuncionarios
        context['listaUsuarios'] = listaUsuarios
        context['listaVisitantes'] = listaVisitantes
        return context


# Base Admin
# Perfil Usuario
def verUsuario(request, username):
    usuario = Usuario.objects.get(username=username)
    personas = Persona.objects.all()
    tipousuario = TipoUsuario.objects.all()
    return render(request, 'perfil.html', {'usuario': usuario, 'personas': personas, 'tipoUsuario': tipousuario})
def contraUsuario(request, username):
    usuario = Usuario.objects.get(username=username)
    personas = Persona.objects.all()
    tipousuario = TipoUsuario.objects.all()
    return render(request, 'cambio_contra.html', {'usuario': usuario, 'personas': personas, 'tipoUsuario': tipousuario})

def editarContraseña(request, username):
    n_contrasena = request.POST.get('password')
    usuario = Usuario.objects.get(username=username)
    user = User.objects.get(username=username)
    try:
        usuario.password = n_contrasena
        usuario.save()
        user.set_password(n_contrasena)
        user.save()
        messages.success(request, 'Contraseña actualizada correctamente!')
    except:
        messages.warning(request, '¡¡Error inesperado: No se actualizo la contraseña!')
    return redirect('/')
# Horario
@user_passes_test(is_funcionario_or_superuser)
def adminHorario(request):
    listaHorarios = Horario.objects.all().order_by('id')
    return render(request, 'adminHorarios.html', {'horarios': listaHorarios})

@user_passes_test(is_superuser)
def registroHorario(request):
    try:
        horaInicio = (datetime.strptime(request.POST['horaInicio'], "%I:%M %p")).strftime("%H:%M:%S")
        horaFin = (datetime.strptime(request.POST['horaFin'], "%I:%M %p")).strftime("%H:%M:%S")

        horario = Horario.objects.create(
            HorarioInicio = horaInicio,
            HorarioFin = horaFin
        )
        messages.success(request,'¡Horario registrado con exito!')  
    except:
        messages.warning(request,'¡Error inesperado: No se registro el horario')
    return redirect('/adminHorario')

@user_passes_test(is_superuser)
def edicionHorario(request, id):
    horario = Horario.objects.get(id=id)
    return render(request, 'edicionHorario.html', {'horario': horario})

@user_passes_test(is_superuser)
def editarHorario(request):
    id = request.POST['horarioId']
    n_horaInicio = (datetime.strptime(request.POST['horaInicio'], "%I:%M %p")).strftime("%H:%M:%S")
    n_horaFin = (datetime.strptime(request.POST['horaFin'], "%I:%M %p")).strftime("%H:%M:%S")
    
    horario = Horario.objects.get(id=id)
    try:
        if not(str(horario.HorarioInicio) == n_horaInicio and str(horario.HorarioFin) == n_horaFin):
            horario.HorarioInicio = n_horaInicio
            horario.HorarioFin = n_horaFin
            horario.estado = True
            horario.save()
    
        horario.estado = True
        horario.save()
        messages.success(request,'¡Horario actualizado!')  
    except:
        messages.warning(request,'¡Error inesperado: No se edito el horario')
    return redirect('/adminHorario')

@user_passes_test(is_superuser)
def eliminarHorario(request,id):
    horario = Horario.objects.get(id=id)
    horario.estado = False
    horario.save()
    messages.success(request,'¡Horario eliminado con exito!')  
    return redirect('/adminHorario')

#---- Tipo Usuario & Roles
@user_passes_test(is_superuser)
def registroRoles(request):
    try:
        # Verificar si el rol ya existe
        existencia_roles = TipoUsuario.objects.filter(Q(nombre='VISITANTE')) and Group.objects.filter(Q(name='VISITANTE')) and Cargo.objects.filter(Q(nombre='GUARDIA')) 
        if existencia_roles.exists():
            messages.warning(request, '¡Ya existen estos registros!')
            return redirect('/adminCargos')
        else:
            TipoUsuario.objects.create(
                    nombre='FUNCIONARIO')     
            Group.objects.create(
                    name='FUNCIONARIO')
            TipoUsuario.objects.create(
                    nombre='GUARDIA') 
            Group.objects.create(
                    name='GUARDIA')
            TipoUsuario.objects.create(
                    nombre='VISITANTE') 
            Group.objects.create(
                name='VISITANTE')
            Cargo.objects.create(
                nombre='GUARDIA'
            )
            messages.success(request,'¡Roles registrados correctamente!')
    except :
        messages.warning(request, '¡SE PRODUJO UN ERROR!')
    return redirect('/adminCargos')

#---- Cargo
@user_passes_test(is_superuser)
def adminCargo(request):
    listaCargos = Cargo.objects.all().order_by('id')
    return render(request, 'adminCargos.html', {'cargos': listaCargos})

@user_passes_test(is_superuser)
def registroCargo(request):
    try:
        nombres = request.POST['nombres'].upper()
        if Cargo.objects.filter(nombre=nombres).exists():
                messages.warning(request,'¡No se registro: El cargo ya existe!')
        else:
            cargo = Cargo.objects.create(
                        nombre=nombres,
                    )     
            messages.success(request,'¡Nueva cargo registrado!')
    except:
        messages.warning(request,'¡Error inesperado: No se registro el cargo')
    return redirect('/adminCargos')

@user_passes_test(is_superuser)
def edicionCargo(request, id):
    cargo = Cargo.objects.get(id=id)
    return render(request, 'edicionCargo.html', {'cargo': cargo})

@user_passes_test(is_superuser)
def editarCargo(request):
    try:
        id = request.POST['funcionarioid']
        n_nombres = request.POST.get('nombres').upper()
        if Cargo.objects.filter(nombre=n_nombres).exclude(id=id).exists():
            messages.warning(request,'¡No se actualizo: El cargo ya existe!')
        else:
            cargo = Cargo.objects.get(id=id)  
            cargo.nombre = n_nombres
            cargo.estado = True
            cargo.save()
            messages.success(request,'¡Cargo actualizado!')
    except:
        messages.warning(request,'¡Error inesperado: No se edito el cargo')
    return redirect('/adminCargos')

@user_passes_test(is_superuser)
def eliminarCargo(request, id):
    cargo = Cargo.objects.get(id=id)
    cargo.estado=False
    cargo.save()
    messages.success(request,'¡Cargo eliminado con exito!')
    return redirect('/adminCargos')


# Validar cedula
def validar_cedula(cedula):
    if not cedula.isdigit() or len(cedula) != 10:
        return False
    provincia = int(cedula[:2])
    if provincia < 1 or provincia > 24:  # Ecuador tiene 24 provincias
        return False
    coeficientes = [2, 1, 2, 1, 2, 1, 2, 1, 2]
    total = 0
    for i, coeficiente in enumerate(coeficientes):
        valor = int(cedula[i]) * coeficiente
        total += valor if valor < 10 else valor - 9
    verificador_calculado = (total % 10) if (total % 10) == 0 else 10 - (total % 10)
    verificador = int(cedula[-1])
    return verificador_calculado == verificador

#Usuario
def visitante(request):
    return render(request, 'registro.html')

def registroVisitante(request):
    nombres = request.POST['nombre'].upper()
    apellidos = request.POST['apellido'].upper()
    cedula = request.POST['cedula']
    correo = request.POST['email']
    telefono = request.POST['celular']
    ciudad = request.POST['ciudad'].upper()
    foto = request.FILES.get('avatar', None)
    contrasena=request.POST['password']

    usuarios= correo
    if not foto:
        foto = Persona._meta.get_field('avatar').get_default()
    if not(validar_cedula(cedula)):
        messages.warning(request,'¡No se registro: Cedula invalidad!')
        return redirect('/visitante')
    elif Persona.objects.filter(cedula=cedula).exists():
        messages.warning(request,'¡No se registro: La cedula ya existe!')
        return redirect('/visitante')
    elif Persona.objects.filter(email=correo).exists():
        messages.warning(request,'¡No se registro: El email ya existe!')
        return redirect('/visitante')
    else:
        persona = Persona.objects.create(
                nombres=nombres,
                apellidos=apellidos,
                cedula=cedula,
                email=correo,
                telefono=telefono,
                ciudad = ciudad,
                avatar = foto,
            )
        # Crear una instancia de Visitante relacionando la Persona 
        visitantes = Visitante.objects.create(
            id_persona=persona,
        )
        tipo_user=TipoUsuario.objects.get(nombre='VISITANTE')
        #-----Asignar Usuario y Tipo de Usuario
        user=Usuario.objects.create(
            id_persona=persona,
            id_tipousuario=tipo_user,
            username=usuarios,
            password=contrasena,
        )
        #-----Asignar Usuario y Grupo
        usuario=User.objects.create(
            username=usuarios,email=correo,first_name=nombres,last_name=apellidos,is_staff="False"
        )
        usuario.set_password(contrasena)
        usuario.save()
        usuario_grupo = Group.objects.get(name='VISITANTE')
        usuario_user = User.objects.get(username=usuarios)
        usuario_user.groups.add(usuario_grupo)
        usuario_user.groups.all()
    messages.success(request,'¡Felicidades ya se encuentra registrado!')    
    return redirect('/')

# Funcionario
@user_passes_test(is_funcionario_or_superuser_or_guardia)
def adminFuncionario(request):
    listaFuncionarios = Funcionario.objects.all().order_by('id')
    listaCargos = Cargo.objects.filter(estado = True).order_by('id')
    listaHorarios = Horario.objects.filter(estado = True).order_by('id')
    return render(request, 'adminFuncionarios.html', {'funcionarios': listaFuncionarios,'cargos': listaCargos, 'horarios':listaHorarios})

@user_passes_test(is_superuser)
def registroFuncionario(request):
    try:
        nombres = request.POST['nombres'].upper()
        apellidos = request.POST['apellidos'].upper()
        cedula = request.POST['cedula']
        correo = request.POST['email']
        telefono = request.POST['telefono']
        cargo_id = int(request.POST['cargo'])
        ciudad = request.POST['ciudad'].upper()
        horarios = request.POST.getlist('horario')
        foto = request.FILES.get('avatar', None)

        usuarios= correo

        if not foto:
            foto = Persona._meta.get_field('avatar').get_default()
        if not(validar_cedula(cedula)):
            messages.warning(request,'¡No se registro: Cedula invalidad!')
            return redirect('/adminFuncionarios')
        elif Persona.objects.filter(cedula=cedula).exists():
            messages.warning(request,'¡No se registro: La cedula ya existe!')
            return redirect('/adminFuncionarios')
        elif Persona.objects.filter(email=correo).exists():
            messages.warning(request,'¡No se registro: El email ya existe!')
            return redirect('/adminFuncionarios')
        else:
            persona = Persona.objects.create(
                    nombres=nombres,
                    apellidos=apellidos,
                    cedula=cedula,
                    email=correo,
                    telefono=telefono,
                    ciudad = ciudad,
                    avatar = foto,
                )
            cargo = Cargo.objects.get(id=cargo_id)

            # Crear una instancia de Funcionario relacionando la Persona y el Cargo
            funcionarios = Funcionario.objects.create(
                id_persona=persona,
                id_cargo=cargo,
            )
            funcionarios.horario.set(horarios)
            funcionarios.save()
            #-----Asignar Usuario y Grupo
            usuario=User.objects.create(
                username=usuarios,email=correo,first_name=nombres,last_name=apellidos,is_staff="False"
            )
            usuario.set_password(cedula)
            usuario.save()
            if cargo.nombre=='GUARDIA':
                empleado_grupo = Group.objects.get(name='GUARDIA')
                tipo_user=TipoUsuario.objects.get(nombre='GUARDIA')
            #-----Asignar Usuario y Tipo de Usuario
            else:
                empleado_grupo = Group.objects.get(name='FUNCIONARIO')
                tipo_user=TipoUsuario.objects.get(nombre='FUNCIONARIO')
            empleado_user = User.objects.get(username=usuarios)
            empleado_user.groups.add(empleado_grupo)
            empleado_user.groups.all()
            user = Usuario.objects.create(
                    id_persona=persona,
                    id_tipousuario=tipo_user,
                    username=usuarios,
                    password=cedula,  
                )
        messages.success(request,'¡Nuevo funcionario registrado!')
    except:
        messages.warning(request,'¡Error inesperado: No se registro el funcionario')
    return redirect('/adminFuncionarios')

@user_passes_test(is_superuser)
def edicionFuncionario(request, id):
    funcionario = Funcionario.objects.get(id=id)
    personas = Persona.objects.all()
    cargo = Cargo.objects.filter(estado = True).order_by('id')
    horarios = Horario.objects.filter(estado = True).order_by('id')
    return render(request, 'edicionFuncionario.html', {'funcionario': funcionario, 'personas': personas, 'cargo': cargo, 'horarios':horarios})

@user_passes_test(is_superuser)
def editarFuncionario(request):
    id = request.POST['funcionarioid']
    n_nombres = request.POST.get('nombres').upper()
    n_apellidos = request.POST.get('apellidos').upper()
    n_email = request.POST.get('email')
    n_telefono = request.POST.get('telefono')
    n_ciudad = request.POST.get('ciudad').upper()
    n_horario = request.POST.getlist('horario')
    n_avatar = request.FILES.get('avatar')
    cargo=Cargo()
    cargo.id = int(request.POST.get('cargo'))
    nueva_cargo=cargo
    funcionario = Funcionario.objects.get(id=id)
    cargo = Cargo.objects.get(id=funcionario.id_cargo.id)
    imagen = funcionario.id_persona.avatar
    try:
        persona = funcionario.id_persona
        coreo_antiguo = funcionario.id_persona.email
        if not(persona.nombres == n_nombres and persona.apellidos == n_apellidos  and persona.email == n_email and persona.ciudad == n_ciudad and persona.telefono == n_telefono and persona.avatar == n_avatar):
            if Persona.objects.filter(email=n_email).exclude(id=funcionario.id_persona.id).exists():
                messages.warning(request,'¡No se registro: El correo ya existe!')
                return redirect('/adminFuncionarios')
            else:
                persona.nombres = n_nombres
                persona.apellidos = n_apellidos
                persona.email = n_email
                persona.telefono = n_telefono
                persona.ciudad = n_ciudad
                if request.POST.get('avatar')=='' :
                    print('no hay imagen')
                    persona.avatar = imagen
                else:
                    persona.avatar = n_avatar
                persona.save()
                funcionario.id_cargo = nueva_cargo
                funcionario.horario.set(n_horario)
                funcionario.estado = True
                funcionario.save()
        messages.success(request, 'Funcionario actualizado correctamente!')
        funcionario.estado = True
        funcionario.horario.set(n_horario)
        funcionario.save()
    except:
         messages.warning(request, '¡¡Error inesperado: No se actualizo el funcionario!')
    return redirect('/adminFuncionarios')

@user_passes_test(is_superuser)
def eliminarFuncionario(request, id):
    funcionario = Funcionario.objects.get(id=id)
    funcionario.estado=False
    funcionario.save()
    messages.success(request,'¡Funcionario eliminado con exito!')
    return redirect('/adminFuncionarios')

from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import JsonResponse
from django.db.models import Count
from datetime import date, timedelta, datetime

@ensure_csrf_cookie
def obtener_fechas_funcionario(request):
    if request.method == 'POST':
        id_funcionario = request.POST.get('id_funcionario', '')
        try:
            fecha_actual = date.today()

            # Consulta para obtener la cantidad de horarios del funcionario
            total_horarios = Funcionario.objects.get(id=id_funcionario).horario.count()

            # Consulta para obtener las fechas que se repiten tres veces para un determinado funcionario
            fechas_repetidas = Solicitud.objects.filter(
                id_funcionario__id=id_funcionario,  # Filtra por el ID del funcionario
                fecha_reservada__gte=fecha_actual,  # Filtra para que la fecha sea mayor o igual a hoy
                estado = True
            ).values('fecha_reservada').annotate(
                total_solicitudes=Count('fecha_reservada')
            ).filter(
                total_solicitudes=total_horarios  # Compara con la cantidad total de horarios
            ).values_list('fecha_reservada', flat=True)
            
            # Formatear las fechas al formato 'YYYY-MM-DD'
            fechas_formateadas = [fecha.strftime('%Y-%m-%d') for fecha in fechas_repetidas]
            print(fechas_formateadas)
            
            
            return JsonResponse({'success': True, 'fechas': list(fechas_formateadas)})
        except Funcionario.DoesNotExist:
            return JsonResponse({'success': False, 'error_message': 'ID de funcionario no proporcionado'})
    
    return JsonResponse({'success': False, 'error_message': 'Método no permitido'})

@ensure_csrf_cookie
def obtener_horarios_funcionario(request):
    if request.method == 'POST':
        id_funcionario = request.POST.get('id_funcionario', '')
        fecha = datetime.strptime(request.POST.get('fecha', ''), "%y-%m-%d").strftime("%Y-%m-%d")
        try:
            # Buscar al funcionario por su ID
            solicitudes = Solicitud.objects.filter(id_funcionario=id_funcionario, fecha_reservada=fecha, estado = True)
            horariosF = Funcionario.objects.get(id=id_funcionario).horario.all()
            # Formatear los horarios de las solicitudes
            horarios_formateados = [
                f'{datetime.strptime(h, "%H:%M").strftime("%H:%M")} - {datetime.strptime(m, "%H:%M").strftime("%H:%M")}'
                for solicitud in solicitudes
                for h, m in [re.findall(r'\b\d{1,2}:\d{2}\b', solicitud.horario)]
            ]
            # Formatear los horarios del funcionario
            horarios_funcionario_formateados = [
                f'{horario.HorarioInicio.strftime("%H:%M")} - {horario.HorarioFin.strftime("%H:%M")}'
                for horario in horariosF
            ]

            # Obtener horarios que no se repiten
            conjunto1 = set(horarios_formateados)
            conjunto2 = set(horarios_funcionario_formateados)
            lista_horarios_no_repetidos = list(conjunto1.symmetric_difference(conjunto2))
            
            # Convierte los horarios a un formato adecuado (por ejemplo, lista de diccionarios)
            horarios_json = [{'inicio': horario.split(' - ')[0], 'fin': horario.split(' - ')[1]} for horario in lista_horarios_no_repetidos]
            
            # Devolver los horarios en formato JSON
            return JsonResponse({'success': True, 'horarios': horarios_json})
        except Funcionario.DoesNotExist:
            # Manejar el caso en el que el funcionario no existe
            return JsonResponse({'success': False, 'error_message': 'Funcionario no encontrado'}, status=404)
    return JsonResponse({'success': False, 'error_message': 'No se recibieron datos válidos'})


def registroSolicitud(request):
    id_Funcionario = int(request.POST['funcionario'])
    visitanteS = request.POST['visitante']
    motivo = request.POST['motivo'].upper()
    horario = request.POST['horario']
    fecha = request.POST['fecha']

    try:
        fecha = datetime.strptime(fecha, "%y-%m-%d")
        fecha = fecha.strftime("%Y-%m-%d")
        # horario = re.findall(r'\b\d{1,2}:\d{2}\b', horario)
        # horario = [datetime.strptime(hora, "%H:%M") for hora in horario]
        # horaInicio = horario[0].strftime("%H:%M:%S")
        # horaFin = horario[1].strftime("%H:%M:%S")

        persona = Persona.objects.get(email = visitanteS)

        visitante = Visitante.objects.get(id_persona = persona )
        print(visitante.id)
        funcionario = Funcionario.objects.get(id=id_Funcionario)

        #Generar codigo unico para el qr

        # Concatenar las variables en una cadena
        cadena_combinada = f"{persona}-{fecha}-{visitante}"

        # Convertir la cadena a una lista de caracteres
        lista_caracteres = list(cadena_combinada)

        # Añadir un carácter aleatorio
        caracter_random = chr(random.randint(33, 126))  # ASCII entre ! y ~
        lista_caracteres.append(caracter_random)

        # Mezclar aleatoriamente los caracteres
        random.shuffle(lista_caracteres)

        # Convertir la lista de caracteres de nuevo a una cadena
        cadena_mezclada = ''.join(lista_caracteres)

        # Calcular el hash MD5 de la cadena mezclada
        hash_md5 = hashlib.md5(cadena_mezclada.encode()).hexdigest()

        solicitud = Solicitud.objects.create(
            id_visitante = visitante,
            id_funcionario = funcionario,
            motivo = motivo,
            fecha_reservada = fecha,
            horario = horario,
            codigo_qr = hash_md5,
        ) 
        solicitud.save()
        messages.success(request,'¡Solicitud registrada con exito!')
    except:
        messages.warning(request,'¡Error inesperado: No se registro la solicitud')
    return redirect('/adminInicioView')

@user_passes_test(is_visitante_or_superuser)
def solicitudes_visitante(request):
    listaFuncionarios = Funcionario.objects.all().order_by('id')
    listaHorarios = Horario.objects.all()
    usuario_logueado = request.user
    listaSolicitud = Solicitud.objects.filter(id_visitante__id_persona__nombres=usuario_logueado.first_name, id_visitante__id_persona__apellidos=usuario_logueado.last_name)
    return render(request, 'solitud_Vistante.html', {'funcionarios': listaFuncionarios,'solicitudes': listaSolicitud, 'horarios':listaHorarios})

@user_passes_test(is_funcionario_or_superuser_or_guardia)
def funcionario_solicitud(request):
    usuario_logueado = request.user
    listaSolicitud = Solicitud.objects.filter(id_funcionario__id_persona__nombres=usuario_logueado.first_name, id_funcionario__id_persona__apellidos=usuario_logueado.last_name).order_by('id')
    return render(request, 'funcionario_solicitud.html', {'solicitudes':listaSolicitud})

def aprobarSolicitud(request, id):
    solicitud = Solicitud.objects.get(id=id)
    solicitud.estado_solicitud = 'aprobado'
    solicitud.save()

    rango_horario = solicitud.horario.split()

    hora_inicio = (datetime.strptime(rango_horario[1], "%H:%M").time()).strftime("%I:%M %p")
    hora_fin = (datetime.strptime(rango_horario[3],"%H:%M").time()).strftime("%I:%M %p")

    data = {
        'funcionario':f'{solicitud.id_funcionario.id_persona.nombres.upper()} {solicitud.id_funcionario.id_persona.apellidos.upper()}.',
        'cargo': solicitud.id_funcionario.id_cargo.nombre,
        'visitante':f'{solicitud.id_visitante.id_persona.nombres.upper()} {solicitud.id_visitante.id_persona.apellidos.upper()}.',
        'estado':solicitud.estado_solicitud.upper(),
        'fecha_reserva':solicitud.fecha_reservada,
        'hora_inicio':hora_inicio,
        'hora_fin':hora_fin,
    }
    email_body = render_to_string('correo.html', data)
    enviarCorreo(
            email_to=solicitud.id_visitante.id_persona.email,
            email_subject=F'[ATENCIÓN] CONFIRMACIÓN DE REUNION CON EL FUNCIONARIO {solicitud.id_funcionario.id_persona.nombres.upper()} {solicitud.id_funcionario.id_persona.apellidos.upper()}.',
            email_body=email_body,
            qr_image_data=generar_codigo_qr(solicitud.codigo_qr)
        )
    return redirect('/funcionario_solicitud')

def rechazarSolicitud(request, id):
    solicitud = Solicitud.objects.get(id=id)
    solicitud.estado_solicitud = 'rechazado'
    solicitud.estado = False
    solicitud.save()
    data = {
        'funcionario':f'{solicitud.id_funcionario.id_persona.nombres.upper()} {solicitud.id_funcionario.id_persona.apellidos.upper()}.',
        'cargo': solicitud.id_funcionario.id_cargo.nombre,
        'visitante':f'{solicitud.id_visitante.id_persona.nombres.upper()} {solicitud.id_visitante.id_persona.apellidos.upper()}.',
        'estado':solicitud.estado_solicitud.upper(),
    }
    email_body = render_to_string('correoR.html', data)
    enviarCorreo2(
            email_to=solicitud.id_visitante.id_persona.email,
            email_subject=F'[ATENCIÓN] SOLICITUD DE REUNION DENEGADA CON EL FUNCIONARIO {solicitud.id_funcionario.id_persona.nombres.upper()} {solicitud.id_funcionario.id_persona.apellidos.upper()}.',
            email_body=email_body,
        )
    return redirect('/funcionario_solicitud')

#Agendamiento directo por parte del funcionario
def registroAgendamiento(request):
    try:
        id_Funcionario = int(request.POST['funcionario'])
        visitanteS = request.POST['visitante']
        motivo = request.POST['motivo'].upper()
        horario = request.POST['horario']
        fecha = request.POST['fecha']

        fecha = datetime.strptime(fecha, "%y-%m-%d")
        fecha = fecha.strftime("%Y-%m-%d")

        print(horario)
        print(visitanteS)
  
        persona = Persona.objects.get(email=visitanteS)
        visitante = Visitante.objects.get(id_persona = persona )
        print(visitante.id)
        funcionario = Funcionario.objects.get(id=id_Funcionario)

        #Generar codigo unico para el qr

        # Concatenar las variables en una cadena
        cadena_combinada = f"{persona}-{fecha}-{visitante}"

        # Convertir la cadena a una lista de caracteres
        lista_caracteres = list(cadena_combinada)

        # Añadir un carácter aleatorio
        caracter_random = chr(random.randint(33, 126))  # ASCII entre ! y ~
        lista_caracteres.append(caracter_random)

        # Mezclar aleatoriamente los caracteres
        random.shuffle(lista_caracteres)

        # Convertir la lista de caracteres de nuevo a una cadena
        cadena_mezclada = ''.join(lista_caracteres)

        # Calcular el hash MD5 de la cadena mezclada
        hash_md5 = hashlib.md5(cadena_mezclada.encode()).hexdigest()

        solicitud = Solicitud.objects.create(
            id_visitante = visitante,
            id_funcionario = funcionario,
            motivo = motivo,
            fecha_reservada = fecha,
            horario = horario,
            codigo_qr = hash_md5,
            estado_solicitud = 'aprobado',
        ) 
        solicitud.save()

        rango_horario = solicitud.horario.split()

        hora_inicio = (datetime.strptime(rango_horario[1], "%H:%M").time()).strftime("%I:%M %p")
        hora_fin = (datetime.strptime(rango_horario[3],"%H:%M").time()).strftime("%I:%M %p")

        data = {
            'funcionario':f'{solicitud.id_funcionario.id_persona.nombres.upper()} {solicitud.id_funcionario.id_persona.apellidos.upper()}.',
            'cargo': solicitud.id_funcionario.id_cargo.nombre,
            'visitante':f'{solicitud.id_visitante.id_persona.nombres.upper()} {solicitud.id_visitante.id_persona.apellidos.upper()}.',
            'estado':solicitud.estado_solicitud.upper(),
            'fecha_reserva':solicitud.fecha_reservada,
            'hora_inicio':hora_inicio,
            'hora_fin':hora_fin,
        }
        email_body = render_to_string('correo.html', data)
        enviarCorreo(
                email_to=solicitud.id_visitante.id_persona.email,
                email_subject=F'[ATENCIÓN] CONFIRMACIÓN DE REUNION CON EL FUNCIONARIO {solicitud.id_funcionario.id_persona.nombres.upper()} {solicitud.id_funcionario.id_persona.apellidos.upper()}.',
                email_body=email_body,
                qr_image_data=generar_codigo_qr(solicitud.codigo_qr)
            )
        
        messages.success(request,'¡Solicitud registrada con exito!')  
    except:
        messages.warning(request,'¡Error inesperado: No se registro la reserva')
    return redirect('/funcionario_solicitud')  


# ESP32-CAM
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt  # Necesario si quieres deshabilitar la protección CSRF para esta vista (¡Ten cuidado!)
def procesar_qr(request):
    if request.method == 'POST':
        qr_code = request.POST.get('qr_code', '')
        print(f'QRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR: {qr_code}')
        try:
            # Intentar obtener la solicitud con el qr_code
            solicitud = Solicitud.objects.get(codigo_qr=qr_code)

            # Verificar y cambiar el estado si es necesario
            if solicitud.estado:
                solicitud.estado = False
                solicitud.estado_solicitud = 'procesado'
                solicitud.save()
                
                registroVisita = ResgistroVisita.objects.create(
                    id_solicitud=solicitud,

                ) 
                return JsonResponse({'success': True, 'message': 'QR Code procesado exitosamente.', 'estado_cambiado': True, 'solicitud_id': solicitud.id})
            else:
                return JsonResponse({'success': False, 'message': 'El QR Code ya ha sido procesado anteriormente.', 'estado_cambiado': False})
        except Solicitud.DoesNotExist:
            # Devolver respuesta JSON indicando que el QR Code no existe en las solicitudes
            return JsonResponse({'success': False, 'message': 'El QR Code no existe en las solicitudes.', 'estado_cambiado': False})
    
    # Devolver respuesta JSON indicando que el QR Code no existe en las solicitudes (por si acaso)
    return JsonResponse({'success': False, 'message': 'El QR Code no existe en las solicitudes.', 'estado_cambiado': False})



def historial(request):
    historialVisitas = ResgistroVisita.objects.all().order_by('id')

    return render(request, 'registroVisitantes.html', {'historial': historialVisitas})


# def aprobarSolicitud(request, id):
#     solicitud = Solicitud.objects.get(id=id)
#     solicitud.estado_solicitud = 'aprobado'
#     solicitud.save()

#     rango_horario = solicitud.horario.split()

#     hora_inicio = (datetime.strptime(rango_horario[1], "%H:%M").time()).strftime("%I:%M %p")
#     hora_fin = (datetime.strptime(rango_horario[3],"%H:%M").time()).strftime("%I:%M %p")

#     data = {
#         'funcionario':f'{solicitud.id_funcionario.id_persona.nombres.upper()} {solicitud.id_funcionario.id_persona.apellidos.upper()}.',
#         'cargo': solicitud.id_funcionario.id_cargo.nombre,
#         'visitante':f'{solicitud.id_visitante.id_persona.nombres.upper()} {solicitud.id_visitante.id_persona.apellidos.upper()}.',
#         'estado':solicitud.estado_solicitud.upper(),
#         'fecha_reserva':solicitud.fecha_reservada,
#         'hora_inicio':hora_inicio,
#         'hora_fin':hora_fin,
#     }
#     email_body = render_to_string('correo.html', data)
#     enviarCorreo(
#             email_to=solicitud.id_visitante.id_persona.email,
#             email_subject=F'[ATENCIÓN] CONFIRMACIÓN DE REUNION CON EL FUNCIONARIO {solicitud.id_funcionario.id_persona.nombres.upper()} {solicitud.id_funcionario.id_persona.apellidos.upper()}.',
#             email_body=email_body,
#             qr_image_data=generar_codigo_qr(solicitud.codigo_qr)
#         )
#     return redirect('/funcionario_solicitud')

