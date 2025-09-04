\# Reserva a visitantes - Sistema de gestión para visitas



\## Descripción del Proyecto



\*\*Reserva a visitantes\*\* es un prototipo de una aplicación web completa (Full-Stack) diseñada para gestionar y automatizar el proceso de reserva y registro de visitantes en una institución. El sistema permite a los funcionarios agendar visitas para invitados, quienes reciben notificaciones por correo electrónico con un código QR único. Este código QR es utilizado para registrar la entrada y salida, simplificando y securizando el acceso.



---



\## Características Principales



\* \*\*Gestión de Usuarios y Roles\*\*: El sistema soporta diferentes tipos de usuarios (Funcionario, Guardia, Visitante) con permisos definidos para cada rol.

\* \*\*Autenticación y Autorización\*\*: Control de acceso a la plataforma basado en roles de usuario.

\* \*\*Reservas de Visitas\*\*: Los funcionarios pueden crear solicitudes de visita para sus invitados, especificando la fecha, horario y motivo.

\* \*\*Generación de Códigos QR\*\*: Se genera un código QR único para cada solicitud de visita, el cual se envía automáticamente por correo electrónico al visitante.

\* \*\*Notificaciones por Correo Electrónico\*\*: Los visitantes reciben un email con los detalles de su reserva y el código QR de acceso.

\* \*\*Registro de Visitas\*\*: Los guardias pueden escanear el código QR para registrar la entrada y salida de los visitantes, asegurando un registro preciso y auditable.

\* \*\*Gestión de Entidades\*\*: Funcionalidades para administrar cargos, horarios y roles de usuario.

\* \*\*Validación de Datos\*\*: Implementación de lógica para validar la cédula y otros datos de los usuarios.



---



\## Tecnologías Utilizadas



Este proyecto fue construido con las siguientes tecnologías:



\* \*\*Backend\*\*: Python, Django 4.2.6

\* \*\*Frontend\*\*: HTML, CSS (AdminLTE), JavaScript

\* \*\*Base de Datos\*\*: PostgreSQL

\* \*\*Otras Bibliotecas\*\*:

&nbsp;   \* `python-dotenv`: Para la gestión de variables de entorno.

&nbsp;   \* `qrcode`: Para la generación de códigos QR.

&nbsp;   \* `smtplib`, `MIMEMultipart`: Para el envío de correos electrónicos.



---



\## Configuración y Ejecución Local



Sigue estos pasos para configurar y ejecutar el proyecto en tu máquina local:



1\.  \*\*Clonar el repositorio\*\*:

&nbsp;   ```bash

&nbsp;   git clone <URL\_del\_repositorio>

&nbsp;   ```



2\.  \*\*Instalar dependencias\*\*:

&nbsp;   Asegúrate de tener Python instalado. Navega a la carpeta del proyecto e instala los paquetes necesarios:

&nbsp;   ```bash

&nbsp;   pip install -r requirements.txt

&nbsp;   ```

&nbsp;   \*Nota: Si no tienes un archivo `requirements.txt`, puedes crearlo manualmente con las dependencias mencionadas en la sección anterior, como Django, python-dotenv, etc.\*



3\.  \*\*Configurar variables de entorno\*\*:

&nbsp;   Crea un archivo `.env` en la carpeta `solicitudes` y agrega tus credenciales de correo electrónico para las notificaciones:

&nbsp;   ```

&nbsp;   EMAIL = tu\_correo@gmail.com

&nbsp;   PASSWORD\_EMAIL = tu\_contraseña\_de\_aplicación

&nbsp;   ```

&nbsp;   \[cite\_start]\*Asegúrate de utilizar una contraseña de aplicación si tienes la verificación en dos pasos activada en tu cuenta de Google. \[cite: 1]\*



4\.  \*\*Configurar la base de datos\*\*:

&nbsp;   El proyecto utiliza PostgreSQL. Configura tu base de datos y actualiza el archivo `settings.py` con tus credenciales.



5\.  \*\*Ejecutar migraciones\*\*:

&nbsp;   Aplica las migraciones para crear las tablas de la base de datos:

&nbsp;   ```bash

&nbsp;   python manage.py makemigrations

&nbsp;   python manage.py migrate

&nbsp;   ```



6\.  \*\*Crear superusuario\*\*:

&nbsp;   Crea un usuario administrador para acceder al panel de administración de Django:

&nbsp;   ```bash

&nbsp;   python manage.py createsuperuser

&nbsp;   ```



7\.  \*\*Ejecutar el servidor de desarrollo\*\*:

&nbsp;   ```bash

&nbsp;   python manage.py runserver

&nbsp;   ```



8\.  \*\*Acceder a la aplicación\*\*:

&nbsp;   Abre tu navegador y ve a `http://127.0.0.1:8000/`.



---



\## Estado del Proyecto



Este es un \*\*prototipo de proyecto de portafolio\*\*. Si bien es funcional, está diseñado para demostrar mis habilidades técnicas en el desarrollo web Full-Stack.



\## Autor



\* Kenny Rodríguez



---

