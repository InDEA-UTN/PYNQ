# 09. Buenas Prácticas y Liberación de Recursos

Trabajar con PYNQ implica administrar tanto la memoria de un entorno Linux como los recursos físicos asignados en la FPGA. A diferencia de un entorno de Python convencional en una PC, en PYNQ dejar recursos colgados puede saturar la placa, bloquear el acceso al hardware o congelar el servidor de Jupyter.

En esta guía veremos las reglas de oro para mantener el sistema estable durante las prácticas de laboratorio.

---

## 1. Liberación Manual de Recursos de Hardware (Buffers y DMA)

Cuando usás `pynq.allocate()`, el sistema operativo reserva bloques de memoria contigua (CMA) que quedan bloqueados exclusivamente para la PL. El recolector de basura de Python no siempre libera esta memoria inmediatamente al terminar una celda.

### Regla General
Siempre liberá los buffers explícitamente cuando dejes de usarlos, especialmente dentro de bucles o al finalizar un experimento.

```python
import pynq
import numpy as np

# 1. Asignación de buffer
buffer_audio = pynq.allocate(shape=(1024,), dtype=np.int32)

# --- Proceso o transferencia vía DMA ---

# 2. Liberación explícita
buffer_audio.freebuffer()
del buffer_audio
```
* **Atención**: Si ejecutas repetidamente una celda con **pynq.allocate()** sin hacer **.freebuffer()**, te quedarás sin memoria CMA disponible (MemoryError / CMA allocation failed).

---

## 2. Gestión de Kernels y Sesiones de Jupyter

Jupyter mantiene el estado de las variables y los recursos cargados en segundo plano aunque cierres la pestaña del navegador.

* **Apagar Kernels Inactivos**: Si terminás de usar un notebook, no te limites a cerrar la pestaña. Ve a la pestaña Running en la interfaz de Jupyter y selecciona Shutdown en el notebook correspondiente.

* **Reiniciar Kernel al Reiniciar Experimentos**: Si cambiaste código que interactúa con la PL y obtenés comportamientos extraños, utilizá la opción Kernel -> Restart & Clear Output.

* **Descarga de Overlays**: Si necesitás cambiar de archivo .bit en el mismo notebook, podés descargar el Overlay activo antes de instanciar el nuevo:

```python
# Liberar el Overlay cargado actualmente
overlay.free()
```

## 3. Prevención de Sobrecalentamiento y Consumo Eléctrico

La FPGA (PL) consume corriente según la complejidad del diseño y la frecuencia de clock de las IPs.

* **Evitá Bucles Infinitos Sin Control**: Un bucle while True: en Python que consulte continuamente un registro por MMIO (overlay.mi_ip.read(0x00)) saturará al procesador ARM al 100%. Introducí pequeñas pausas con time.sleep() para reducir la carga de CPU y la temperatura del chip.

* **Lógica en Reposo**: Si tenés IPs de alto procesamiento en la PL, asegurate de detener los timers o desactivar el Enable cuando no estés capturando datos.

## 4. Control de Versiones (Git con .ipynb)

Los archivos .ipynb de Jupyter guardan no solo el código, sino también salidas pesadas, imágenes renderizadas y metadatos en formato JSON. Esto genera conflictos de fusión (merge conflicts) difíciles de resolver.

**Prácticas Recomendadas para el Repositorio**

* **Limpiar Salidas antes de Commit**: Antes de subir un notebook a Git, ejecutá Cell -> All Output -> Clear para mantener el repositorio liviano.

* **Ignorar Archivos Pesados en .gitignore**: Asegurate de incluir lo siguiente en tu .gitignore:
```plaintext
# Archivos temporales de Jupyter
.ipynb_checkpoints/

# Bitstreams pesados o temporales de Vivado (si aplica)
*.runs/
*.supp/
```
---

[← Anterior: 08. Flujo de trabajo, persistencia y Git](./01_flujo_de_trabajo.md)