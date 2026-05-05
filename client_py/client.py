import socket, time, os

HOST = os.getenv("TARGET_HOST")
PORT = int(os.getenv("TARGET_PORT"))
MY_UID = os.getenv("USER_ID")  # Pastikan USER_ID diset dalam docker-compose.yml

while True:
    try:
        c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        c.connect((HOST, PORT))
        
        # Hantar ID kepada server supaya server tahu siapa yang mahu update mata
        if MY_UID:
            c.send(MY_UID.encode())
            
        c.close()
        print(f"Berjaya menghantar signal untuk {MY_UID} ke {HOST}")
    except Exception as e:
        print(f"Gagal berhubung: {e}")
        
    time.sleep(10)
