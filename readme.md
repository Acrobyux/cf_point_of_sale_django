# Sistema de Gestión de Ventas para Bazares Temporales

Este proyecto es un sistema de gestión diseñado para negocios que participan en bazares temporales. Permite llevar un registro de ventas, administrar el inventario y gestionar campañas específicas por cada bazar.

## Características Principales

- Registro de ubicaciones y flyers para los bazares temporales.
- Creación de campañas para representar cada bazar.
- Control de inventario y ganancias por producto.
- Etiquetado de productos con ID para un registro preciso de ventas.
- Gestión de categorías para organizar los productos.
- Notificaciones automáticas via e-mail a clientes sobre nuevas campañas.

## Requisitos

- Python 3.9+
- Django 4.2
- Virtualenv (recomendado)

## Instalación

1. Clona este repositorio: `git clone https://github.com/Acrobyux/cf_point_of_sale_django.git`
2. Ve al directorio del proyecto: `cd tu-proyecto`
3. Crea un entorno virtual (opcional pero recomendado): `virtualenv venv`
4. Activa el entorno virtual: 
    - En Windows: `venv\Scripts\activate`
    - En macOS y Linux: `source venv/bin/activate`
5. Instala las dependencias: `pip install -r requirements.txt`
6. Configura las variables de entorno (ver sección "Configuración" abajo).

## Configuración

1. Crea un archivo `.env` en el directorio raíz del proyecto.
2. Define las variables de entorno en el archivo `.env`:
    - EMAIL_HOST_USER
    - EMAIL_HOST_PASSWORD
3. Define en el archivo `settings.py` tu configuracion de servidor de correos.
4. En el archivo `settings.py` busca la constante `STATICFILES_DIRS` debe contener la ruta absoluta 
   a la carpeta `static` (de los archivos estaticos)
5. Si no se ven reflejados los cambios del archivo `.env` en la aplicacion reinicia el servidor.

## Uso

1. Ejecuta las migraciones: `python manage.py migrate`
2. Crea un superusuario: `python manage.py createsuperuser`
    - Nota: El nombre y apellidos del superusuario son utiles en el proyecto.
    - Nota: El superusuario debe tener e-mail para que le llegue copia de los correos enviados.
3. Inicia el servidor de desarrollo: `python manage.py runserver`
4. Abre tu navegador en `http://127.0.0.1:8000/` para ver el proyecto.
5. Inicia sesion con las credenciales de tu `superuser`
