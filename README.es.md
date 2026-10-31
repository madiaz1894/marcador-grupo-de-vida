# Marcador de Parejas · Grupo de Vida

[English](README.md) · **Español**

Un marcador para noches de juegos, para mostrar en un televisor o proyector. Lleva el puntaje de dos equipos (por defecto **Hombres** y **Mujeres**) a lo largo de varios juegos. Incluye un juego de charadas, timbres de trivia en el celular de cada equipo y un control remoto en el iPhone para que quien dirige pueda manejarlo todo desde la mano.

Son tres páginas HTML y un pequeño servidor en Python. No hay que instalar ni compilar nada; el servidor solo usa la biblioteca estándar de Python.

| Archivo | Qué es |
| --- | --- |
| `marcador.html` | El marcador que se ve en el televisor |
| `remote.html` | El control remoto de quien dirige (se abre en un iPhone) |
| `buzzer.html` | Un timbre de trivia, un celular por equipo |
| `server.py` | Sirve las páginas y conecta los celulares con el marcador por Wi‑Fi |
| `Iniciar marcador.command` | Para abrir con doble clic en macOS |
| `Iniciar marcador.bat` | Para abrir con doble clic en Windows |

## Funciones

### Marcador
- Dos equipos con nombres editables, y un título editable para la noche.
- Cada juego tiene su propio puntaje, y el total de la noche suma todos los juegos.
- **Lista de juegos de la noche**: escribe los juegos de la noche, uno por línea (ej. Charadas, Pictionary, Trivia de parejas). Cada vez que empiezas un juego nuevo, toma el siguiente nombre de la lista.
- Suma o resta puntos con el teclado, con botones rápidos (−1, +1, +2, +3, +5, +10) o con cualquier cantidad.
- **Deshacer** (hasta 100 pasos) y reinicio completo.
- Efectos de celebración al anotar puntos (confeti, fuegos artificiales, corazones, estrellas y más), con efectos de sonido que se pueden apagar.
- **Pantalla final**: "Y el equipo ganador de la noche es…" anuncia al ganador, o el empate.
- Tres estilos visuales: **Noche Luxe**, **Gala Dorada** y **Estadio**.
- Modo de pantalla completa. El cursor y los controles se ocultan tras unos segundos sin mover el mouse.
- Todo se guarda automáticamente en el navegador, así que cerrar o recargar la página no borra el puntaje.

### Panel de control (tecla `C` o el botón ⚙︎)
Solo aparece en pantalla mientras está abierto. Desde aquí puedes:
- Cambiar el título, los nombres de los equipos y el nombre del juego actual.
- Sumar puntos, empezar un juego nuevo, deshacer, reiniciar y mostrar la pantalla final.
- Manejar las charadas y el timbre de trivia.
- Elegir un estilo, activar o apagar el sonido y poner pantalla completa.
- Ver los códigos QR del control remoto y de los dos timbres (solo si lo abriste con el servidor, ver abajo).

### Charadas
- Un mazo de unas 100 palabras en español, barajado. Las palabras no se repiten hasta que se acaba el mazo.
- Turnos con tiempo: 30 s, 45 s, 60 s, 90 s, 2 min o el tiempo que quieras.
- Hay una cuenta regresiva y luego las palabras salen una por una. Cada palabra adivinada da +1 punto al equipo en turno.
- Puedes pasar una palabra, pausar o seguir, deshacer la última palabra adivinada o terminar el turno antes.

### Timbre de trivia
- Cada equipo abre `buzzer.html` en un celular (escaneando su código QR). Gana quien presione primero; el servidor decide quién fue primero, así que la velocidad del celular no importa.
- Quien dirige marca la respuesta como **Correcto** (los puntos van al equipo automáticamente) o **Incorrecto** (ese equipo queda bloqueado y el otro equipo puede intentar).
- Puntos por respuesta correcta: 1, 2, 3 o 5.

### Control remoto en el iPhone
- Escanea el código QR del panel de control para abrir el control en tu celular.
- Muestra el puntaje en vivo y permite sumar o restar puntos, empezar un juego nuevo, mostrar la pantalla final y manejar las charadas y el timbre de trivia.
- Las acciones que ve todo el salón (juego nuevo, pantalla final) piden dos toques para confirmar.
- Un código de 4 dígitos en el enlace evita que otras personas en el mismo Wi‑Fi controlen el marcador. El código se guarda en `.codigo`, así que los celulares no tienen que volver a escanear después de reiniciar.

## Cómo abrirlo

El marcador se puede usar de dos maneras:

- **Con el servidor (recomendado):** funciona todo, incluido el control del iPhone y los timbres de trivia. Necesita Python 3.
- **Sin el servidor:** abre `marcador.html` con doble clic en el navegador. Funcionan el puntaje, las charadas, los estilos y la pantalla final, pero no el control del celular ni los timbres.

El computador necesita internet para las fuentes y los códigos QR. Los celulares deben estar en la **misma red Wi‑Fi** que el computador.

### macOS
1. Python 3 normalmente viene con macOS. Si te pide instalar las "herramientas de desarrollo de línea de comandos", acepta, o instala Python desde [python.org](https://www.python.org/downloads/).
2. Haz doble clic en **`Iniciar marcador.command`**.
   - La primera vez, macOS puede bloquearlo. Haz clic derecho sobre el archivo → **Abrir** → **Abrir**.
   - Si dice que no tienes permiso, ejecuta `chmod +x "Iniciar marcador.command"` en la Terminal desde esta carpeta.
3. El marcador se abre en el navegador. Deja la ventana de la Terminal abierta mientras juegan.

O desde la Terminal: `python3 server.py`

### Windows
1. Instala Python 3 desde [python.org](https://www.python.org/downloads/). Durante la instalación, marca **"Add python.exe to PATH"**.
2. Haz doble clic en **`Iniciar marcador.bat`**.
3. Cuando el Firewall de Windows pregunte, permite el acceso en **Redes privadas**. Si no, los celulares no se podrán conectar.
4. El marcador se abre en el navegador. Deja la ventana negra abierta mientras juegan.

O desde una terminal: `py server.py` (o `python server.py`)

### Linux
Ejecuta `python3 server.py` desde esta carpeta.

### En el televisor
1. Conecta el computador al televisor (HDMI, AirPlay, etc.) y pasa la ventana del navegador a esa pantalla.
2. Presiona `F` para pantalla completa.
3. Presiona `C` para abrir el panel de control y escanea el código QR del control remoto (y de los timbres si van a jugar trivia).
4. Presiona `C` otra vez para ocultar el panel.

El servidor usa el puerto 8000. Para usar otro, define la variable de entorno `PORT`, por ejemplo `PORT=8080 python3 server.py`. Para que no abra el navegador automáticamente, define `NO_BROWSER=1`.

## Atajos de teclado

Presiona `?` en el marcador para verlos en pantalla.

| Tecla | Acción |
| --- | --- |
| `Q` / `A` | Equipo 1 +1 / −1 (con `Shift`, ±5) |
| `P` / `L` | Equipo 2 +1 / −1 (con `Shift`, ±5) |
| `N` | Empezar un juego nuevo |
| `Z` | Deshacer |
| `W` | Mostrar la pantalla final (ganador) |
| `C` | Abrir / cerrar el panel de control |
| `T` | Siguiente estilo |
| `F` | Pantalla completa |
| `S` | Sonido sí / no |
| `H` | Abrir charadas |
| `B` | Trivia: nueva pregunta (activa los timbres) |
| `Y` / `X` | Trivia: correcto / incorrecto |
| `?` | Ver los atajos |
| `Esc` | Cerrar lo que esté abierto |

**Durante las charadas:**

| Tecla | Acción |
| --- | --- |
| `Espacio` | Iniciar / pausar |
| `→` o `Enter` | Palabra adivinada (+1) |
| `←` | Pasar palabra |
| `Retroceso` | Deshacer la última palabra adivinada |
| `1` / `2` | Elegir el equipo en turno |
| `Esc` o `H` | Cerrar las charadas |
