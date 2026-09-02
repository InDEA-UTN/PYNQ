import socket
import os

HOST = '0.0.0.0'
PUERTO = 5005

def iniciar_servidor_udp():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PUERTO))
        print(f"[*] Escuchando notificaciones de la PYNQ...")
        
        while True:
            datos, (ip_origen, puerto_origen) = s.recvfrom(1024)
            mensaje = datos.decode('utf-8')
            
            # Responder ACK directamente a la IP y PUERTO desde el que la PYNQ envió el mensaje
            s.sendto(b"ACK", (ip_origen, puerto_origen))
            
            # Notificación en Ubuntu
            os.system(f'notify-send "PYNQ-Z2 Conectada" "IP: {ip_origen}\nAcceso: http://{ip_origen}:9090" --icon=network-workgroup')
            print(f"[!] IP Recibida: {ip_origen}. Confirmación enviada.")

if __name__ == "__main__":
    iniciar_servidor_udp()