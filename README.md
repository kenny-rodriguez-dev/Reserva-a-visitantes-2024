\# Reserva a visitantes - Sistema de gestión para visitas



\## Descripción del Proyecto



\*\*Reserva a visitantes\*\* es un prototipo de una aplicación web completa (Full-Stack) diseñada para gestionar y automatizar el proceso de reserva y registro de visitantes en una institución. El sistema permite a los funcionarios agendar visitas para invitados, quienes reciben notificaciones por correo electrónico con un código QR único. Este código QR es utilizado para registrar la entrada y salida, simplificando y asegurando el acceso.



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


\* \*\*Frontend\*\*: HTML, CSS (AdminLTE), JavaScript

\* \*\*Backend\*\*: Python, Django 4.2.6

\* \*\*Base de Datos\*\*: PostgreSQL

\* \*\*Otras Bibliotecas\*\*:

&nbsp;   \* `python-dotenv`: Para la gestión de variables de entorno.

&nbsp;   \* `qrcode`: Para la generación de códigos QR.

&nbsp;   \* `smtplib`, `MIMEMultipart`: Para el envío de correos electrónicos.



---



\## Configuración y Ejecución Local



Siga estos pasos para configurar y ejecutar el proyecto en su máquina local:



1\.  \*\*Clonar el repositorio\*\*:

&nbsp;   ```bash

&nbsp;   git clone \[https://github.com/su-usuario/reserva-a-visitantes-2024.git](https://github.com/su-usuario/reserva-a-visitantes-2024.git)

&nbsp;   ```



2\.  \*\*Instalar dependencias\*\*:

&nbsp;   Asegúrese de tener Python instalado. Navegue a la carpeta del proyecto e instale los paquetes necesarios:

&nbsp;   ```bash

&nbsp;   pip install -r libreria.txt

&nbsp;   ```



3\.  \*\*Configurar variables de entorno\*\*:

&nbsp;   Debe crear un archivo `.env` en la carpeta `solicitudes` y agregar sus credenciales de correo electrónico para las notificaciones:

&nbsp;   ```

&nbsp;   EMAIL = su\_correo@gmail.com

&nbsp;   PASSWORD\_EMAIL = su\_contraseña\_de\_aplicación

&nbsp;   ```

&nbsp;   \*Asegúrese de utilizar una contraseña de aplicación si tiene la verificación en dos pasos activada en su cuenta de Google. \*



4\.  \*\*Configurar la base de datos\*\*:

&nbsp;   El proyecto utiliza PostgreSQL. Configure su base de datos y actualice el archivo `settings.py` con sus credenciales.



5\.  \*\*Ejecutar migraciones\*\*:

&nbsp;   Aplique las migraciones para crear las tablas de la base de datos:

&nbsp;   ```bash

&nbsp;   python manage.py makemigrations

&nbsp;   python manage.py migrate

&nbsp;   ```



6\.  \*\*Crear superusuario\*\*:

&nbsp;   Debe crear un usuario administrador para acceder al panel de administración de Django:

&nbsp;   ```bash

&nbsp;   python manage.py createsuperuser

&nbsp;   ```



7\.  \*\*Ejecutar el servidor de desarrollo\*\*:

&nbsp;   ```bash

&nbsp;   python manage.py runserver

&nbsp;   ```



8\.  \*\*Acceder a la aplicación\*\*:

&nbsp;   Debe abrir su navegador y dirigirse a `http://127.0.0.1:8000/`.



---



\## Estado del Proyecto



Este es un \*\*prototipo de proyecto de gestión para visitas\*\*. Si bien es funcional, está diseñado para demostrar mis habilidades técnicas en el desarrollo web Full-Stack.



\## Autor



\* Kenny Rodríguez

\* https://www.linkedin.com/in/kennyrodriguezm/



---

