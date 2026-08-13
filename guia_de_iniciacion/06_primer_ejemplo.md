# 06. Primer Ejemplo: Ejecución de punta a punta y Análisis Técnico

En este módulo realizaremos la creación y ejecución de un Notebook en Jupyter para interactuar por primera vez con los periféricos de la **PYNQ-Z2** controlados desde la FPGA. Analizaremos paso a paso el código Python y lo que sucede a nivel de hardware.

---

## 1. Crear un Nuevo Notebook

1. Ingresa a la interfaz de Jupyter Notebook desde tu navegador
2. En la esquina superior derecha, haz clic en **New** -> **Python 3 (ipykernel)**.
3. Renombra el notebook como `01_primer_ejemplo.ipynb`.

---

## 2. Código Completo del Ejemplo (Parpadeo e Interacción de LEDs)

Copia y ejecuta las siguientes celdas de código en tu notebook:

### Celda 1: Importación y carga del Overlay Base
```python
from pynq.overlays.base import BaseOverlay
import time

# Cargamos el Overlay precompilado que maneja los periféricos de la placa
base = BaseOverlay('base.bit')
print("Overlay base cargado exitosamente en la FPGA.")
```

### Celda 2: Control de LEDs y Conmutadores (Switches)
```python
# Asignamos referencias a los LEDs y Switches integrados en la placa
led0 = base.leds[0]
led1 = base.leds[1]
sw0 = base.switches[0]

print("Iniciando bucle de control... Cambia la posición del Switch SW0 en la placa.")

# Ejecutamos un bucle por 10 segundos
for _ in range(100):
    if sw0.read() == 1:
        led0.on()
        led1.off()
    else:
        led0.off()
        led1.on()
    time.sleep(0.1)

# Apagamos ambos LEDs al finalizar
led0.off()
led1.off()
print("Ejecución finalizada.")
```

---

## 3. Explicación Detallada:

Para entender el flujo completo de este ejemplo, desglosaremos lo que ocurrió desde la celda de Python hasta la respuesta del silicio:

```text
[ Python / Jupyter ]  -->  [ Librería PYNQ (MMIO) ]  -->  [ Kernel Linux ]  -->  [ Bus AXI-Lite ]  -->  [ IP Core AXI GPIO (FPGA) ]  -->  [ Pin Físico / LED ]
```

### Paso 1: Carga del Bitstream (`BaseOverlay('base.bit')`)
1. La función `BaseOverlay` invoca al driver de PYNQ en Linux para reprogramar la FPGA a través de la interfaz **DevC / ICAP** (*Internal Configuration Access Port*).
2. Se envía el archivo binario `.bit` a la *Programmable Logic* (PL). El LED **DONE (`LD12`)** confirma que las puertas lógicas se configuraron.
3. PYNQ lee el archivo de metadatos `.hwh` e instanció internamente los controladores para el mapa de memoria AXI.

### Paso 2: Abstracción de Objetos (`base.leds[0]`, `base.switches[0]`)
* Los LEDs y Switches no están conectados directamente al procesador ARM (PS), sino a pines de la FPGA (PL).
* La FPGA incluye un bloque IP denominado **AXI GPIO** (General Purpose I/O mapeado en memoria).
* `base.leds[0]` representa una instancia de la clase `LED` de PYNQ, la cual abstrae la dirección física de memoria base del módulo AXI GPIO (ejemplo: `0x41200000`).

### Paso 3: Lectura y Escritura (`sw0.read()`, `led0.on()`)
* Al ejecutar `sw0.read()`, Python realiza una lectura a través de la capa **MMIO** (*Memory-Mapped I/O*) leyendo el registro de entrada del puerto GPIO correspondiente en el bus AXI.
* Al ejecutar `led0.on()`, Python escribe un bit '1' en el registro de salida AXI GPIO. La lógica interna de la FPGA pone en alto (3.3V) el pin físico mapeado al LED0 de la placa.

---

## 4. Experimento Adicional: Control de LEDs RGB

Prueba este bloque adicional para controlar el LED RGB integrado (`LD4` o `LD5`):

```python
# Instancia del LED RGB 4
rgb_led = base.rgbleds[4]

# Colores disponibles: 0=Off, 1=Blue, 2=Green, 3=Cyan, 4=Red, 5=Magenta, 6=Yellow, 7=White
print("Ciclando colores en el LED RGB 4...")
for color in range(1, 8):
    rgb_led.write(color)
    time.sleep(0.5)

rgb_led.write(0) # Apagar
```

---

## 5. Conclusiones
* **Sin escribir VHDL/Verilog**, hemos reconfigurado la FPGA y tomado control en tiempo real de sus terminales de entrada/salida.
* Toda la comunicación entre el procesador ARM y la FPGA ocurre de forma transparente mediante el bus estándar industrial **AXI4-Lite** y mapas de memoria administrados por Python.
