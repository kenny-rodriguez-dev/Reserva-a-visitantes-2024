# Enviar correo 
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

import qrcode
from io import BytesIO
# Variables de entorno
import os
from dotenv import load_dotenv

# Cargar las variables desde el archivo .env
load_dotenv()


def generar_codigo_qr(valor):
    # Generar la imagen QR
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(f'{valor}')
    qr.make(fit=True)
    qr_image = qr.make_image(fill_color="black", back_color="white")
    qr_image_buffer = BytesIO()
    # Convertir la imagen QR de PNG a JPG
    qr_image = qr_image.convert('RGB')
    # Guardar la imagen en formato JPG
    qr_image.save(qr_image_buffer, format='JPEG')
    # Obtener los datos de la imagen QR en formato bytes
    qr_image_data = qr_image_buffer.getvalue()

    return qr_image_data

def enviarCorreo(email_to, email_subject,email_body, qr_image_data):
    # Configurar el servidor SMTP
    smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
    smtp_server.starttls()
    smtp_server.login(os.getenv("EMAIL"), os.getenv("PASSWORD_EMAIL"))

    # Crear el mensaje de correo electrónico
    message = MIMEMultipart()
    message['Subject'] = email_subject
    message['From'] = os.getenv("EMAIL")
    message['To'] = email_to

    # Agregar el cuerpo del correo electrónico como HTML
    html_body = MIMEText(email_body, 'html')
    message.attach(html_body)

    # Agregar la imagen del código QR como un adjunto
    qr_image_attachment = MIMEImage(qr_image_data)
    qr_image_attachment.add_header('Content-ID', '<qr_image>')
    qr_image_attachment.add_header('Content-Disposition', 'inline', filename='qr.jpg')
    message.attach(qr_image_attachment)

    # Enviar el correo electrónico
    smtp_server.sendmail(os.getenv("EMAIL"), email_to, message.as_string())

    # Cerrar la conexión con el servidor SMTP
    smtp_server.quit()


def enviarCorreo2(email_to, email_subject,email_body):
    # Configurar el servidor SMTP
    smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
    smtp_server.starttls()
    smtp_server.login(os.getenv("EMAIL"), os.getenv("PASSWORD_EMAIL"))

    # Crear el mensaje de correo electrónico
    message = MIMEMultipart()
    message['Subject'] = email_subject
    message['From'] = os.getenv("EMAIL")
    message['To'] = email_to

    # Agregar el cuerpo del correo electrónico como HTML
    html_body = MIMEText(email_body, 'html')
    message.attach(html_body)



    # Enviar el correo electrónico
    smtp_server.sendmail(os.getenv("EMAIL"), email_to, message.as_string())

    # Cerrar la conexión con el servidor SMTP
    smtp_server.quit()