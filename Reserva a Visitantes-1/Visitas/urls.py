"""
URL configuration for Visitas project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from solicitudes import views
from django.conf import settings
from django.conf.urls.static import static
from solicitudes.views import LoginFormView,LogoutView,adminInicioView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('',views.inicio,name='inicio')
    path('', LoginFormView.as_view(),name="login"),
    path('logout/', LogoutView.as_view(),name="logout"),

    #inicioAdmin
    path('adminInicioView/',login_required(adminInicioView.as_view()), name='adminInicio'),
    #Perfil de usuario
    path('verUsuario/<username>', login_required(views.verUsuario), name='verUsuario'),
    path('contraUsuario/<username>', login_required(views.contraUsuario), name='contraUsuario'),
    path('editarContraseña/<username>', login_required(views.editarContraseña), name='editarContraseña'),

    #Horarios
    path('adminHorario/', login_required(views.adminHorario), name='adminHorario'),
    path('registroHorario/', login_required(views.registroHorario), name='registroHorario'),
    path('edicionHorario/<id>', login_required(views.edicionHorario), name='edicionHorario'),
    path('editarHorario/', login_required(views.editarHorario), name='editarHorario'),
    path('eliminarHorario/<id>', login_required(views.eliminarHorario), name='eliminarHorario'),

    #Cargos
    path('adminCargos/', login_required(views.adminCargo), name='adminCargo'),
    path('registroRoles/', login_required(views.registroRoles), name='registroRoles'),
    path('registroCargo/', login_required(views.registroCargo), name='registroCargo'),
    path('edicionCargo/<id>', login_required(views.edicionCargo), name='edicionCargo'),
    path('editarCargo/', login_required(views.editarCargo), name='editarCargo'),
    path('eliminarCargo/<id>', login_required(views.eliminarCargo), name='eliminarCargo'),

    #Funcionarios
    path('adminFuncionarios/', login_required(views.adminFuncionario), name='adminFuncionario'),
    path('registroFuncionario/', login_required(views.registroFuncionario), name='registroFuncionario'),
    path('edicionFuncionario/<id>', login_required(views.edicionFuncionario), name='edicionFuncionario'),
    path('editarFuncionario/', login_required(views.editarFuncionario), name='editarFuncionario'),
    path('eliminarFuncionario/<id>', login_required(views.eliminarFuncionario), name='eliminarFuncionario'),

    path('obtener_horarios_funcionario/', login_required(views.obtener_horarios_funcionario), name='obtener_horarios_funcionario'),
    path('obtener_fechas_funcionario/', login_required(views.obtener_fechas_funcionario), name='obtener_fechas_funcionario'),

    path('registroSolicitud/', login_required(views.registroSolicitud), name='registroSolicitud'),
    path('registroAgendamiento/', login_required(views.registroAgendamiento), name='registroAgendamiento'),
    path('solicitudes_visitante/', login_required(views.solicitudes_visitante), name='solicitudes_visitante'),
    path('funcionario_solicitud/', login_required(views.funcionario_solicitud), name='funcionario_solicitud'),
    path('aprobarSolicitud/<id>', login_required(views.aprobarSolicitud), name='aprobarSolicitud'),
    path('rechazarSolicitud/<id>', login_required(views.rechazarSolicitud), name='rechazarSolicitud'),

    #Visitante
    path('visitante/', views.visitante, name='visitante'),
    path('registroVisitante/', views.registroVisitante, name='registroVisitante'),

    # ESP32-CAM
    path('procesar_qr/', views.procesar_qr, name='procesar_qr'),
    path('historial/', views.historial, name='historial'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
