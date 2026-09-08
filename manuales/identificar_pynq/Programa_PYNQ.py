import socket
import time

PUERTO = 5005
BROADCAST_IP = '<broadcast>'

def notificar_con_confirmacion():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.settimeout(2.0)

    for intento in range(30):
        try:
            # 1. Obtenemos el nombre del host o la IP asignada
            ip_placa = None
            try:
                ip_placa = socket.gethostbyname(socket.gethostname())
            except Exception:
                pass
            
            # Si gethostbyname devuelve loopback, usamos un mensaje genérico temporal
            if not ip_placa or ip_placa.startswith('127.'):
                # Forzamos un socket para ver la IP de la interfaz
                aux = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                aux.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
                aux.connect(('10.255.255.255', 1)) # IP privada genérica
                ip_placa = aux.getsockname()[0]
                aux.close()

            mensaje = f"Placa PYNQ-Z2 lista. Acceso: http://{ip_placa}:9090"
            print(f"[Intento {intento+1}] IP detectada: {ip_placa}. Enviando...")

            # 2. Enviar Broadcast
            s.sendto(mensaje.encode('utf-8'), (BROADCAST_IP, PUERTO))
            
            # 3. Esperar confirmación ACK
            respuesta, addr = s.recvfrom(1024)
            if "ACK" in respuesta.decode('utf-8', errors='ignore').upper():
                print(f" -> Confirmación recibida desde {addr}. Deteniendo envíos.")
                break

        except (socket.timeout, OSError) as e:
            print(f" -> Reintentando ({e})...")
            time.sleep(2)

    s.close()

if __name__ == "__main__":
    notificar_con_confirmacion()