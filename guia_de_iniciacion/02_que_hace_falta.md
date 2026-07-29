# 02. Requisitos Previos: Hardware y Software Necesarios

Para comenzar a trabajar con la placa **PYNQ-Z2**, es necesario contar con una serie de componentes de hardware y herramientas de software indispensables para su puesta en marcha y configuración inicial.

---

## 1. Hardware Necesario

### Placa y Alimentación
* **Placa de desarrollo PYNQ-Z2** (TUL Corporation).
* **Fuente de alimentación de 5V DC / 3A (Plug DC 2.1mm):** 
  * *Nota:* La placa se puede alimentar vía Micro-USB (poniendo el jumper `JP7` en posición `USB`), pero para cargas de trabajo exigentes o uso de periféricos en los puertos USB Host/HDMI, se recomienda usar una fuente externa dedicada de 5V por el conector jack DC (jumper `JP7` en posición `REG`).

### Almacenamiento y Conectividad
* **Tarjeta MicroSD (Mínimo 16 GB, Clase 10 / UHS-I recomendada):**
  * Se utilizará para flashear la imagen del sistema operativo Linux + PYNQ.
* **Cable Ethernet (RJ45):**
  * Necesario para conectar la placa a la red local (router/switch) o directamente a la tarjeta de red de la PC para acceder al entorno Jupyter Notebook vía web.
* **Cable Micro-USB a USB-A:**
  * Para la interfaz USB-UART (consola serie) y depuración/alimentación USB básica.
* **Lector de tarjetas MicroSD:**
  * Para conectar la tarjeta MicroSD a la computadora host y flashear la imagen.

### Periféricos Opcionales (Según la aplicación)
* **Cable HDMI:** Si se planea trabajar con procesamiento de video (entrada/salida).
* **Cables/Audífonos de 3.5mm:** Para aplicaciones de procesamiento de audio en tiempo real.

---

## 2. Software Necesario

### En la Computadora Host (PC)

1. **Imagen de Disco de PYNQ-Z2:**
   * Archivo de imagen `.img` oficial distribuido por PYNQ (versión compatible para PYNQ-Z2, ejecutable sobre Ubuntu/Linux embebido).
2. **Herramienta de Flasheo de Tarjetas SD:**
   * **BalenaEtcher** (Recomendado por su simplicidad en Windows/Linux/macOS) o **Raspberry Pi Imager** / `dd`.
3. **Cliente de Consola Serie / Terminal:**
   * **PuTTY** (Windows) o `screen` / `minicom` / `picocom` (Linux/macOS) para conectarse a la consola de comandos de la PYNQ-Z2 vía UART (Baudrate: `115200`).
4. **Navegador Web Moderno:**
   * Google Chrome, Mozilla Firefox o Microsoft Edge para acceder a la interfaz de **Jupyter Notebook** (`http://192.168.2.99` o `http://pynq:9090`).
5. **Entorno de Desarrollo de Hardware (Opcional - Para desarrollo avanzado):**
   * **AMD/Xilinx Vivado ML Standard Edition** (para crear Overlays personalizados, sintetizar bloques IP o realizar flujos HLS).

---

## 3. Checklist Antes de Empezar

- [ ] Tarjeta MicroSD flasheada con la imagen oficial de PYNQ.
- [ ] Jumper de arranque (`JP1`) configurado en la posición **SD**.
- [ ] Jumper de alimentación (`JP7`) configurado según la fuente elegida (**USB** o **REG**).
- [ ] Cable Ethernet conectado entre la PYNQ-Z2 y la PC / Router.
- [ ] Placa alimentada y LEDs de estado encendidos (`DONE` iluminado tras el arranque).
