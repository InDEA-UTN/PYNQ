import socket
import time

PUERTO = 5005
BROADCAST_IP = '<broadcast>'

def obtener_ip_local():
    """Obtiene la IP local sin requerir salida a Internet ni consultar servidores externos."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Apunta a la dirección de broadcast local 
        s.connect(('255.255.255.255', 1))
        ip = s.getsockname()[0]
        s.close()
        if not ip.startswith('127.'):
            return ip
    except Exception:
        pass
    return None

def notificar_con_confirmacion():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.settimeout(2.0)  # Espera máximo 2 segundos por respuesta

    for intento in range(30):
        # 1. Obtener la IP local de forma segura dentro del bucle
        ip_placa = obtener_ip_local()
        
        # Si la red aún no asignó una IP, esperar y reintentar
        if not ip_placa:
            time.sleep(2)
            continue

        mensaje = f"Placa PYNQ-Z2 lista. Acceso: http://{ip_placa}:9090"

        try:
            # 2. Enviar Broadcast
            s.sendto(mensaje.encode('utf-8'), (BROADCAST_IP, PUERTO))
            
            # 3. Esperar confirmación de la PC
            respuesta, addr = s.recvfrom(1024)
            
            # Verificación flexible de la respuesta ACK
            if "ACK" in respuesta.decode('utf-8', errors='ignore').upper():
                print("La PC confirmó la recepción. Deteniendo envíos.")
                break
        except (socket.timeout, OSError):
            # Si la PC no responde o la interfaz de red está negociando, reintentar
            time.sleep(2)

    s.close()

if __name__ == "__main__":
    notificar_con_confirmacion()