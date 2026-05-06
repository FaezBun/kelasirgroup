import os, socket, threading, mysql.connector
import sys

PORT = int(os.getenv("PORT", 6001))

def handle_client(c, addr):
    print(f"[CONNECTED] {addr} connected.")
    try:
        # Terima data dengan timeout supaya server tidak tergantung
        c.settimeout(5.0) 
        client_uid = c.recv(1024).decode().strip()
        
        if client_uid:
            print(f"[INFO] Receiving update request for: {client_uid}")
            
            # Sambungan Database
            conn = mysql.connector.connect(
                host="db", 
                user="root", 
                password="rootpassword", 
                database="socket_db"
            )
            cursor = conn.cursor()
            
            # Gunakan parameterized query untuk mengelakkan SQL Injection
            sql = "UPDATE user_points SET points = points + 1 WHERE user = %s"
            cursor.execute(sql, (client_uid,))
            conn.commit()
            
            print(f"[SUCCESS] Updated {client_uid}. Rows affected: {cursor.rowcount}")
            cursor.close()
            conn.close()
        else:
            print(f"[WARNING] Received empty UID from {addr}")
            
    except Exception as e:
        print(f"[ERROR] Transaction failed for {addr}: {e}")
    finally:
        c.close()
        print(f"[DISCONNECTED] {addr} closed.")

# Main Server Loop
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Supaya port cepat release
s.bind(('0.0.0.0', PORT))
s.listen(10)
print(f"[STARTING] Server listening on port {PORT}...")

while True:
    try:
        c, addr = s.accept()
        threading.Thread(target=handle_client, args=(c, addr), daemon=True).start()
    except KeyboardInterrupt:
        print("\n[SHUTDOWN] Server stopping...")
        s.close()
        sys.exit()
