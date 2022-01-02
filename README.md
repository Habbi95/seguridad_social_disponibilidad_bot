# seguridad_social_disponibilidad_bot
Bot hecho con Selenium para rellenar el formulario de la Seguridad Social y buscar disponibilidad de citas.

Echa un vistazo al script ss_notifier.py y rellena con tus datos. Necesitas el chromewebdriver y tener instaladas las dependencias.

El script rellenará el formulario de la SS con tus datos y consultará si hay citas disponibles. De ser asi hará un pantallazo y te lo enviará por correo.

Puedes integrarlo en un crontab para hacer la tarea periodica. 

Puedes user task_ss.sh en un crontab, obviamente modifica la ruta de donde se active tu virtual env y donde este el script principal. 
