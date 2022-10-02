from celery import Celery

celery_app= Celery(__name__, broker='redis://localhost:6379/0')

@celery_app.task(name='registrar_log')
def registrar_log(usuario, fecha, acceso):
    with open('authorization_log','a+') as file:
        if acceso==1:
           file.write('Usuario Autorizado: {} Fecha: {}\n'.format(usuario, fecha))
        elif acceso==2:
           file.write('Usuario Desautorizado(Signature verification failed): {} Fecha: {}\n'.format(usuario, fecha))
        elif acceso==3:
           file.write('Usuario Desautorizado(Missing Token): {} Fecha: {}\n'.format(usuario, fecha))           
        elif acceso==4:
           file.write('Usuario Desautorizado(Error General): {} Fecha: {}\n'.format(usuario, fecha))
        elif acceso==5:
           file.write('Ataque a la confidencialidad detectado - usuario: {} Fecha: {}\n'.format(usuario, fecha))           
        else:
           file.write('Usuario Desautorizado: {} Fecha: {}\n'.format(usuario, fecha))
