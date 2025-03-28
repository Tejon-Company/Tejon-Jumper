# Tejón Jumper

Tejón Jumper es un juego de plataformas en 2D desarrollado para la asignatura de Contornos Inmersivos, Interactivos y de Entrenimiento de la Universidade da Coruña.

Para más detalles sobre este proyecto, se puede consultar la memoria, disponible en la carpeta _docs_.

## Autores
- __Faro Pérez, Inés__
- __Gómez Tejón, Marcos__
- __Maciel Montero, Claudia__
- __Rey López, Carolina__
- __Suárez Calvo, Esteban__

## Manual de usuario

### Instalación

#### Requisitos previos

- Tener instalado __Python 3.12__ o superior.
- Tener __pip__ instalado y actualizado para la gestión de paquetes.
- Opcionalmente, se recomienda utilizar un entorno virtual para evitar conflictos entre dependencias.

#### Instalación

Es posible instalar todas las dependencias del juego utilizando el archivo _requirements.txt_, que contiene las versiones necesarias de cada paquete.

Para instalar los paquetes automáticamente, se debe ejecutar el siguiente comando en la terminal, dentro del directorio donde se encuentra el archivo:

`pip install -r requirements.txt`

#### Uso del entorno virtual (opcional)

Se recomienda crear un entorno virtual para el proyecto. Para ello, ejecutar el siguiente comando dentro del directorio del juego:

`python -m venv venv`

Luego, para activar el entorno virtual:

- En Windows:

`venv\Scripts\activate`

- En Linux:

`source venv/bin/activate`

Una vez activado, instalar las dependencias del requirements.txt con el comando mencionado anteriormente.

#### Ejecución del juego

Para ejecutar el juego, basta con situarse en la carpeta del proyecto y ejecutar el archivo principal con el siguiente comando:

`python main.py`

### Controles

- __Mover al tejón__: Flechas izquierda y derecha.

- __Saltar__: Flecha de arriba.

- __Rodar__: Shift (solo cuando la barra de energía esté llena).

- __Pausar el juego__: Tecla p o Esc.