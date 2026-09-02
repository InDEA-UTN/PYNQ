import socket
import time

PUERTO = 5005
BROADCAST_IP = '<broadcast>'

def notificar_con_confirmacion():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.settimeout(2.0) # Espera máximo 2 segundos por respuesta

    # Obtener IP local activa...
    aux = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    aux.connect(('8.8.8.8', 80))
    ip_placa = aux.getsockname()[0]
    aux.close()

    mensaje = f"Placa PYNQ-Z2 lista. Acceso: http://{ip_placa}:9090"

    for intento in range(12):
        try:
            # 1. Enviar Broadcast
            s.sendto(mensaje.encode('utf-8'), (BROADCAST_IP, PUERTO))
            
            # 2. Esperar confirmación de la PC
            respuesta, addr = s.recvfrom(1024)
            if respuesta.decode('utf-8') == "ACK":
                print("La PC confirmó la recepción. Deteniendo envíos.")
                break # Se detiene inmediatamente
        except socket.timeout:
            # Si la PC aún no está encendida o escuchando, reintenta en 5s
            time.sleep(5)
            
    s.close()

if __name__ == "__main__":
    notificar_con_confirmacion()