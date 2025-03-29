# Tejón Jumper 🎮🚀

Tejón Jumper es un juego de plataformas en 2D desarrollado para la asignatura de **Contornos Inmersivos, Interactivos y de Entrenimiento (CIIE)**, cursada en último curso del grado en Ingeniería Informática, en la mención de Computación.

El personaje principal del videojuego es un pequeño tejón que habita en el bosque, el cual va recorriendo a lo largo de tres niveles, recolectando bayas y enfrentándose a diversos enemigos (zorros, erizos, murciélagos, ardillas y setas), para terminar el juego entrentándose al jefe final, el oso.

Para más detalles sobre este proyecto, se puede consultar la memoria, disponible en la carpeta _docs_.

## Autores 💪👥

- **Faro Pérez, Inés**
- **Gómez Tejón, Marcos**
- **Maciel Montero, Claudia**
- **Rey López, Carolina**
- **Suárez Calvo, Esteban**

## Manual de usuario 📝📚

### Instalación 🔧🛠️

#### Requisitos previos ✅

- Tener instalado **Python 3.12** o superior.

- Tener **pip** instalado y actualizado para la gestión de paquetes.

#### Guía de instalación 📦

Una vez cumplimos con los requisitos previos, se deben instalar las dependencias del juego, para lo que se facilita el fichero [requirements.txt](requirements.txt)

>[!TIP]
>
>A pesar de no ser estrictamente necesario, antes de instalar las dependencias, se recomienda crear un entorno virtual. Este paso es recomendable para evitar posibles conflictos con otros paquetes ya instalados en nuestra máquina.

Para crear el entorno virtual: `python -m venv venv`

Para activar el entorno virtual:

- En windows: `venv\Scripts\activate`

- En linux: `source venv/bin/activate`

Para instalar las dependencias de forma automática: `pip install -r requirements.txt`

#### Ejecución del juego 🎮

Para ejecutar el juego, basta con situarse en la carpeta del proyecto y ejecutar el archivo principal con el siguiente comando: `python src/main.py`

> [!NOTE]
>
> El videojuego se puede ejecutar en 2 resoluciones diferentes, 1280x720 y 1880x1030. Por defecto el videojuego se ejecuta en 1280x720, para modificar la resolución es necesario dirigirse a la pantalla de ajustes.
>
> Además, la resolución en 1880x1030 puede mostrarse de forma incorrecta si el usuario tiene activado el escalado en los ajustes de pantalla de su ordenador, por lo que si es el caso, se recomienda, o bien jugar en la otra resolución, o bien desactivar el escalado.

### Controles 🕹️🎮

- **Mover al tejón**. Flechas izquierda y derecha.

- **Saltar**. Barra espaciadora o flecha arriba.

- **Rodar**. Shift (solo cuando la barra de energía esté llena).

- **Pausar el juego**. Tecla p o Esc.
