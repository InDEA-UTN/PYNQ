# 08. Flujo de Trabajo, Persistencia y Git

Una vez que sabés cómo conectarte y correr tu primer notebook, es momento de organizar el trabajo diario. Dado que PYNQ ejecuta un sistema operativo Ubuntu Linux completo sobre su procesador ARM (PS), podés usar herramientas estándar de desarrollo directamente en la placa.

En esta guía veremos cómo transferir archivos, gestionar el almacenamiento local y vincular la placa con GitHub para subir tus prácticas mediante Pull Requests.

---

## 1. Organización de Archivos y Persistencia

Por defecto, el servidor de Jupyter inicia en el directorio raíz del usuario `xilinx`:

```text
/home/xilinx/jupyter_notebooks/
```

### Reglas de Oro para Guardar el Trabajo

* **Trabajá dentro de tu propia carpeta**: Creá una subcarpeta con tu nombre o el nombre de tu proyecto dentro de jupyter_notebooks/ para mantener el sistema limpio.

* **Respaldá tu código frecuentemente**: La memoria MicroSD almacena todo el sistema operativo y tus archivos localmente. Si la tarjeta se corrompe o se reinstala la imagen base de la placa, perderás los datos locales. Usá siempre Git o SFTP para respaldar tu trabajo.
## 2. Transferencia de Archivos (SFTP / SCP)

Si necesitás subir o bajar datasets, archivos .bit, audios o imágenes pesadas, moverlos a través de la interfaz web de Jupyter puede resultar incómodo o lento.

### Opción A: Cliente SFTP (WinSCP / FileZilla)

Podés conectarte mediante SFTP desde tu PC utilizando los datos de conexión estándar de la PYNQ:

* **Protocolo**: SFTP

* **Host**: IP de la PYNQ (o pynq)

* **Puerto**: 22

* **Usuario**: xilinx

* **Contraseña**: xilinx

### Opción B: Comando scp desde Consola Local

Desde la terminal de tu computadora personal podés transferir archivos directamente:
```bash
# Copiar un archivo local hacia la PYNQ
scp archivo_local.bit xilinx@pynq:/home/xilinx/jupyter_notebooks/

# Copiar una carpeta desde la PYNQ hacia tu PC
scp -r xilinx@pynq:/home/xilinx/jupyter_notebooks/mi_proyecto ./
```
## 3. Acceso por Consola (SSH y Terminal Web)

Para administrar paquetes o ejecutar comandos de Linux, podés abrir una terminal de dos formas:

1. Desde Jupyter: En el menú principal de la interfaz web, seleccioná New -> Terminal.

2. Vía SSH desde tu PC:

```bash
ssh xilinx@pynq
```
Desde la terminal podés monitorear el consumo de CPU y memoria con htop, revisar logs del sistema o ejecutar comandos de Git.

## 4. Integración con Git y GitHub (Claves SSH y Pull Requests)

Para GitHub, la PYNQ funciona como cualquier otra computadora con Linux. Podés clonar repositorios, realizar commits y abrir Pull Requests directamente desde la consola de la placa.

### Paso 1: Configurar la identidad en la PYNQ

Abrí una terminal en la PYNQ y definí tus datos de usuario:

```bash
git config --global user.name "Tu Nombre u Usuario"
git config --global user.email "tu_email@ejemplo.com"
```

### Paso 2: Generar una clave SSH en la placa

Para autenticarte contra GitHub sin escribir tu contraseña en cada interacción:

```bash
ssh-keygen -t ed25519 -C "pynq-lab-board"
```
*(Presioná Enter en todas las preguntas para confirmar la ubicación y opciones por defecto).*

### Paso 3: Cargar la clave SSH en GitHub

1. Muestra en pantalla el contenido de la clave pública creada:

```bash
cat ~/.ssh/id_ed25519.pub
```
2. Copiá todo el texto impreso en la terminal.

3. Ingresá a tu cuenta de GitHub desde el navegador -> Settings -> SSH and GPG keys -> New SSH key.

4. Pegá la clave copiada, asignale un nombre descriptivo (ej. Placa PYNQ Lab) y guardala.

### Paso 4: Flujo de Trabajo con Git y Pull Requests

1. **Clonar el repositorio mediante SSH:**

```bash
git clone git@github.com:usuario/nombre-repositorio.git
cd nombre-repositorio
```

2. **Crear una rama nueva para la práctica:**

```bash
git checkout -b practica-1-filtros
```
3. **Registrar y commitear los cambios realizados en Jupyter:**

```bash
git add .
git commit -m "Agrego resolución del ejercicio 1"
```
4. **Subir la rama a GitHub:**

```bash
git push -u origin practica-1-filtros
```
5. **Crear el Pull Request**:
Ingresá a la página del repositorio en GitHub desde tu computadora personal. Verás una notificación indicando que subiste una rama recientemente junto al botón "Compare & pull request". Hacé clic allí para solicitar la revisión del código.

## 5. Instalación de Paquetes Adicionales (pip)

Si tu proyecto requiere librerías de Python no incluidas en la imagen base de PYNQ (como scikit-learn o librosa), podés instalarlas mediante la terminal de la placa:
```bash
pip install nombre-libreria
```
**Atención**: La PYNQ tiene recursos de procesamiento y RAM limitados. **La instalación de librerías grandes que requieran compilación en C/C++ puede demorar varios minutos.**

---

[← Anterior: 07. Primer ejemplo](./07_primer_ejemplo.md) | [Siguiente: 09. Buenas prácticas →](./09_buenas_practicas.md)