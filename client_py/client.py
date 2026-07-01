import socket, time, os

HOST = os.getenv("TARGET_HOST")
PORT = int(os.getenv("TARGET_PORT"))
MY_UID = os.getenv("USER_ID")  # Pastikan USER_ID diset dalam docker-compose.yml

# WAJIB guna flush=True supaya log terus dihantar ke Docker
print(f"[PYTHON CLIENT {MY_UID}] Memulakan client... Sasaran: {HOST}:{PORT}", flush=True)

while True:
    try:
        c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(f"[PYTHON CLIENT {MY_UID}] Cuba menyambung ke server...", flush=True)
        
        c.connect((HOST, PORT))
        
        # Hantar ID kepada server supaya server tahu siapa yang mahu update mata
        if MY_UID:
            c.send(MY_UID.encode())
            print(f"[PYTHON CLIENT {MY_UID}] Berjaya menghantar signal ID '{MY_UID}' ke {HOST}", flush=True)
            
            # TERIMA POINT DB DARI SERVER
            response = c.recv(1024).decode().strip()
            
            if response:
                print(f"[PYTHON CLIENT {MY_UID}] Point DB Terkini: {response}", flush=True)
            else:
                print(f"[PYTHON CLIENT {MY_UID}] Tiada respon point dari server.", flush=True)
                
        c.close()
        print(f"[PYTHON CLIENT {MY_UID}] Soket ditutup. Tunggu 10 saat...\n{'-'*50}", flush=True)
        
    except Exception as e:
        print(f"[PYTHON CLIENT {MY_UID}] Gagal berhubung: {e}\n{'-'*50}", flush=True)
        
    time.sleep(10)
