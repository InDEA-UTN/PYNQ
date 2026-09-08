import socket
import os

HOST = '0.0.0.0'
PUERTO = 5005

def iniciar_servidor_udp():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PUERTO))
        print("[*] Escuchando notificaciones de la PYNQ-Z2...")
        
        while True:
            datos, (ip_origen, puerto_origen) = s.recvfrom(1024)
            # Decodificar el mensaje enviado por la placa
            mensaje = datos.decode('utf-8', errors='ignore').strip()
            
            # 1. Enviar confirmación ACK a la placa
            s.sendto(b"ACK", (ip_origen, puerto_origen))
            
            # 2. Imprimir en consola el mensaje recibido
            print("\n" + "="*50)
            print(f"[!] {mensaje}")
            print("="*50 + "\n")
            
            # 3. Mostrar notificación emergente usando el mensaje parseado de la PYNQ
            os.system(f'notify-send "PYNQ-Z2 Conectada" "{mensaje}" --icon=network-workgroup')

if __name__ == "__main__":
    iniciar_servidor_udp()