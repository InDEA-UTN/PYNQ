# 04. Preparar la Placa: Grabado de Imagen, Configuración de Jumpers y Primer Encendido

En este apartado se detalla el procedimiento paso a paso para preparar la tarjeta MicroSD, configurar correctamente los *jumpers* de hardware de la **PYNQ-Z2** y realizar el primer encendido exitoso de la placa.

---

## Paso 1: Grabar la Imagen de PYNQ en la Tarjeta MicroSD

1. **Descargar la imagen oficial:**
   * Obtener la última versión de la imagen `.img` para PYNQ-Z2 desde el sitio web oficial de PYNQ ([pynq.io](http://www.pynq.io/)).
2. **Conectar la MicroSD:**
   * Insertar la tarjeta MicroSD (mínimo 16 GB) en la computadora host mediante un lector de tarjetas.
3. **Flashear la imagen:**
   * Abrir **BalenaEtcher** (o la herramienta de preferencia).
   * Seleccionar la imagen descrita (`pynq_z2_vX.X.img`).
   * Seleccionar la unidad correspondiente a la tarjeta MicroSD.
   * Hacer clic en **Flash!** y esperar a que finalice el proceso de grabado y verificación.
4. **Extraer de forma segura:**
   * Una vez terminado el proceso, expulsar la MicroSD de la PC e insertarla en el zócalo MicroSD ubicado en la parte inferior de la placa PYNQ-Z2.

---

## Paso 2: Configuración de Jumpers en la PYNQ-Z2

Antes de conectar la alimentación, es crítico verificar la posición de los *jumpers* de selección en la placa:

```text
       +-----------------------------------------------+
       |  JP1 (Boot Source)  --> Seleccionar "SD"     |
       |  JP7 (Power Source) --> Seleccionar "USB/REG"|
       +-----------------------------------------------+
```

### 1. Fuente de Arranque (`JP1` - Boot Selection)
* Colocar el jumper `JP1` en la posición **SD**. Esto le indica al chip Zynq-7000 que cargue el bootloader (FSBL) y el sistema operativo desde la tarjeta MicroSD en lugar de la memoria Flash JTAG o QSPI.

### 2. Fuente de Alimentación (`JP7` - Power Selection)
* **Opción A (USB):** Si se alimenta la placa mediante el puerto Micro-USB (PROG/UART), colocar `JP7` en la posición **USB**.
* **Opción B (REG - Recomendado):** Si se utiliza una fuente de alimentación externa de 5V DC mediante el conector jack, colocar `JP7` en la posición **REG** (Regulador interno).

### 3. Configuración del Bus USB Host (`JP4` / `JP5`)
* Asegurarse de que los jumpers de control USB estén colocados en posición por defecto para permitir la operación del puerto USB Host si se conectan periféricos.

---

## Paso 3: Conexiones de Cables y Primer Encendido

1. **Conectar el cable de red (Ethernet):**
   * Conectar un extremo del cable RJ45 al puerto Ethernet de la PYNQ-Z2 y el otro al router de la red local o directamente a la tarjeta de red del PC.
2. **Conectar el cable Micro-USB:**
   * Conectar el cable Micro-USB al puerto rotulado como **PROG / UART** de la placa y a un puerto USB de la PC (esto proveerá comunicación serie por consola y alimentación si `JP7` está en USB).
3. **Encender la placa:**
   * Deslizar el interruptor de encendido **SW0 / POWER** a la posición **ON**.

---

## Paso 4: Verificación del Proceso de Boot (LEDs de Estado)

Al encender la placa, se debe observar la siguiente secuencia en los LEDs integrados:

1. **Power LED (`LD13` / Red):** Se enciende inmediatamente en rojo continuo, indicando que la placa recibe energía.
2. **DONE LED (`LD12` / Green):** Después de unos segundos (~5-10 s), el LED **DONE** se ilumina en verde. Esto confirma que la lógica reconfigurable (FPGA) cargó exitosamente el *bitstream* base.
3. **LEDs de actividad del procesador:** Los LEDs de usuario o del puerto Ethernet parpadearán indicando el arranque del kernel de Linux Ubuntu y la inicialización de los servicios de Jupyter Notebook (el proceso completo toma alrededor de 30 a 45 segundos).


## Diagnóstico Rápido de Problemas (Troubleshooting)

* **El LED DONE no se enciende:**
  * Verificar que la tarjeta MicroSD esté firmemente asentada.
  * Confirmar que el jumper `JP1` esté configurado en la posición **SD**.
  * Re-flashear la imagen en la tarjeta MicroSD usando BalenaEtcher.
* **La placa se reinicia intermitentemente:**
  * Si se alimenta por USB, la PC o puerto USB puede no estar entregando la corriente suficiente (mínimo 2A-3A). Cambiar a un cargador de pared dedicado o usar una fuente jack DC de 5V (jumper `JP7` en **REG**).

---

[← Anterior: 03. Que hace falta](./03_que_hace_falta.md) | [Siguiente: 05. Conectarse →](./05_conectarse.md)