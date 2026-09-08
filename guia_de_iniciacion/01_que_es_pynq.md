# Introducción a PYNQ (*Python Productivity for Zynq*)

**PYNQ** (*Python Productivity for Zynq*) es un **framework de código abierto desarrollado por AMD/Xilinx** que permite programar sistemas heterogéneos —los cuales combinan procesadores ARM y lógica reconfigurable FPGA— utilizando **Python** en lugar de lenguajes de descripción de hardware tradicionales (HDLs) como VHDL o Verilog.

En términos sencillos: es la **capa de software y abstracción** que conecta el entorno de programación de alto nivel (Python/Jupyter) con la potencia de cómputo en paralelo de la FPGA.

---

## Arquitectura y Funcionamiento Interno

PYNQ no elimina la FPGA ni traduce Python directamente a puertas lógicas en tiempo real. En su lugar, utiliza una arquitectura basada en **Overlays** (superposiciones o aceleradores de hardware precompilados).

```text
+-------------------------------------------------------+
|                Aplicación en Python                   |
|           (Jupyter Notebooks / Scripts)               |
+-------------------------------------------------------+
                           |
                           v
+-------------------------------------------------------+
|                    Librería PYNQ                      |
|      (Mapeo de memoria, Drivers C/C++, CFFI)          |
+-------------------------------------------------------+
                           |
                           v
+-------------------------------------------------------+
|              Sistema Operativo Linux                  |
|          (Ubuntu corriendo en el procesador ARM)      |
+-------------------------------------------------------+
                           |
                           v
+-------------------------------------------------------+
|              Hardware Heterogéneo (Zynq)              |
|   [ Processing System (ARM) | Programmable Logic ]    |
|                             |   (Overlay / Bitstream) |
+-------------------------------------------------------+
```
Los Overlays se pueden pensar como si fueran librerias en C (por ejemplo, stdio.h o math.h) pero que en vez de describir funciones, describen el funcionamiento de un circuito electronico digital, configurando la interconexion de transistores/puertas lógicas en la FPGA

### Componentes Clave

1. **Linux Embebido y Jupyter Server:** La placa ejecuta una distribución de Ubuntu Linux sobre los núcleos ARM del *Processing System* (PS). En este entorno corre un servidor de **Jupyter Notebook**, permitiendo programar, iterar y visualizar resultados desde un navegador web.
2. **Librería de Python (`pynq`):** Proporciona la API para interactuar con la FPGA desde Python:
   * Cargar bitstreams dinámicamente (`overlay = Overlay('design.bit')`).
   * Acceder a registros e interrupciones mediante variables y métodos directos.
   * Transferir arreglos de datos a alta velocidad mediante DMA (*Direct Memory Access*) e interfaces AXI.

---

## Comparativa de Enfoques

| Aspecto | Enfoque Tradicional en FPGA | Enfoque con PYNQ |
| :--- | :--- | :--- |
| **Lenguaje principal** | VHDL / Verilog / C++ (HLS) | Python (integrado con NumPy, OpenCV, etc.) |
| **Flujo de desarrollo** | Síntesis, P&R y simulación pesada para cada cambio | Carga de Overlays precompilados e iteración en Python |
| **Entorno de prueba** | Compilación de hardware y depuración por JTAG | Ejecución interactiva celda por celda en Jupyter |
| **Manejo de E/S y datos** | Control manual de registros y drivers bare-metal | Abstracción de alto nivel (`pynq.lib`, DMA buffers) |

---

## Ejemplo Básico de Uso en Python

A continuación se muestra un ejemplo de cómo se inicializa un *Overlay*, se asigna memoria compartida y se realiza la transferencia de datos mediante DMA a un acelerador en la FPGA:

```python
from pynq import Overlay, allocate
import numpy as np

# 1. Cargar el Overlay (bitstream) en la FPGA
ol = Overlay('my_accelerator.bit')

# 2. Reservar memoria contigua para transferencia DMA (usando xnk/pynq allocate)
input_buffer = allocate(shape=(1024,), dtype=np.int32)
output_buffer = allocate(shape=(1024,), dtype=np.int32)

# 3. Inicializar datos de entrada
input_buffer[:] = np.arange(1024, dtype=np.int32)

# 4. Enviar datos al acelerador por DMA y recibir el resultado
dma = ol.axi_dma_0
dma.sendchannel.transfer(input_buffer)
dma.recvchannel.transfer(output_buffer)
dma.sendchannel.wait()
dma.recvchannel.wait()

print("Procesamiento completado en hardware.")
```

---

## Perfiles de Uso

* **Desarrolladores de Software y Científicos de Datos:** Permite acelerar algoritmos de procesamiento de señales (DSP), visión artificial y aprendizaje automático aprovechando la lógica reconfigurable sin necesidad de dominar sintaxis VHDL/Verilog ni flujos de síntesis de hardware.
* **Diseñadores de Hardware:** Permite modularizar y empaquetar bloques IP como componentes reutilizables en Python, facilitando la integración, verificación y distribución de aceleradores a equipos de software.

---

[Siguiente: 02. Conceptos claves sobre la PYNQ →](./02_conceptos_claves_pynq.md)