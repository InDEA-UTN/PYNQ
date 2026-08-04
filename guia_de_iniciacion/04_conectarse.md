# 04. Conectarse a la Placa: Red y Acceso a Jupyter Notebook

Una vez encendida la placa **PYNQ-Z2** con el sistema operativo inicializado, el siguiente paso es conectarse a ella a través de la red para acceder al entorno de desarrollo web **Jupyter Notebook** o por línea de comandos mediante **SSH** y **UART**.

---

## 1. Métodos de Conexión a la Red

Existen dos topologías principales para conectar la PYNQ-Z2 a tu computadora:

### Opción A: Conexión vía Router/Switch (Red Local - Recomendado)
1. Conecta el cable Ethernet desde la PYNQ-Z2 a un puerto LAN de tu router.
2. Tu PC debe estar conectada a la misma red (por Wi-Fi o cable).
3. El servidor DHCP del router le asignará automáticamente una dirección IP a la placa.

### Opción B: Conexión Directa PC a Placa (Punto a Punto)
1. Conecta el cable Ethernet directamente desde el puerto RJ45 de la PYNQ-Z2 a la tarjeta de red de tu PC.
2. La placa tiene configurada por defecto la dirección IP estática **`192.168.2.99`**.
3. En tu PC, debes configurar la interfaz de red Ethernet en la misma subred (por ejemplo, IP: `192.168.2.1`, Máscara de red: `255.255.255.0`).

---

## 2. Acceso al Entorno Jupyter Notebook

1. Abre un navegador web moderno (Chrome, Firefox o Edge).
2. En la barra de direcciones, ingresa una de las siguientes URLs:
   * **Por nombre de host (si el router soporta mDNS):**
     ```text
     http://pynq:9090
     ```
   * **Por dirección IP estática (conexión directa):**
     ```text
     http://192.168.2.99:9090
     ```
   * **Por dirección IP dinámica (asignada por DHCP):**
     ```text
     http://<IP_ASIGNADA_POR_ROUTER>:9090
     ```
3. **Autenticación:**
   * **Contraseña por defecto:** `xilinx`

---

## 3. Acceso por Consola SSH y Terminal Serie (UART)

### Acceso vía SSH
* **Comando:** `ssh xilinx@pynq` o `ssh xilinx@192.168.2.99`
* **Usuario:** `xilinx`
* **Contraseña:** `xilinx`

### Acceso vía UART (Consola Micro-USB)
Si no tienes conexión de red, puedes acceder al sistema operativo Linux por consola serie:
1. Conecta el cable Micro-USB al puerto PROG/UART de la placa.
2. Abre **PuTTY** (en Windows) o tu terminal favorita (en Linux/macOS).
3. Configura los parámetros de conexión serie:
   * **Puerto:** `COMx` (Windows) / `/dev/ttyUSBx` (Linux)
   * **Baudrate / Velocidad:** `115200`
   * **Data bits:** `8` | **Stop bits:** `1` | **Parity:** `None`

---

## 4. ¿Qué hacer si Jupyter o la placa no aparecen? (Troubleshooting)

Si no puedes acceder a `http://pynq:9090` o la IP no responde, sigue estos pasos de diagnóstico en orden:

### Diagnóstico 1: Comprobar el estado físico (LEDs)
* **LED DONE (LD12):** Debe estar encendido en **verde**. Si está apagado, la FPGA no cargó la imagen y el procesador no arrancó. Revisa la tarjeta MicroSD y el jumper `JP1` (debe estar en **SD**).
* **LEDs del puerto Ethernet:** Comprueba que los LEDs del puerto RJ45 parpadeen (indica enlace físico y tráfico).

### Diagnóstico 2: Descubrir la IP asignada por DHCP
Si usas router y `http://pynq:9090` no resuelve:
1. Conéctate por terminal serie (UART) con PuTTY.
2. Presiona Enter e inicia sesión (Usuario: `xilinx`, Clave: `xilinx`).
3. Ejecuta el comando:
   ```bash
   ifconfig eth0
   ```
4. Busca el valor `inet` para obtener la dirección IP exacta asignada y accede desde el navegador indicando esa IP con el puerto `:9090`.

### Diagnóstico 3: Problemas en Conexión Directa PC-Placa
1. Si conectaste el cable Ethernet directamente a la PC, abre la configuración de red de Windows/Linux.
2. Desactiva temporalmente el Wi-Fi para evitar conflictos de métrica de rutas.
3. Asegúrate de que la interfaz de red Ethernet de tu PC tenga una IP fija configurada en el rango `192.168.2.X` (por ejemplo, `192.168.2.10`), con máscara `255.255.255.0`.
4. Haz un ping a la placa desde la consola de comandos de tu PC:
   ```cmd
   ping 192.168.2.99
   ```

### Diagnóstico 4: Conflicto de Firewall / Antivirus
* Asegúrate de que el puerto `9090` no esté bloqueado por el Firewall de Windows o antivirus de tu PC.
* Prueba agregar la regla de entrada o desactivar temporalmente el firewall para verificar.
