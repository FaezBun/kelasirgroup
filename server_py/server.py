import os, socket, threading, mysql.connector
import sys

PORT = int(os.getenv("PORT", 6001))

def handle_client(c, addr):
    print(f"[CONNECTED] {addr} connected.", flush=True)
    try:
        # Terima data dengan timeout supaya server tidak tergantung
        c.settimeout(5.0) 
        client_uid = c.recv(1024).decode().strip()
        
        if client_uid:
            print(f"[INFO] Receiving update request for: {client_uid}", flush=True)
            
            # Sambungan Database
            conn = mysql.connector.connect(
                host="db", 
                user="root", 
                password="rootpassword", 
                database="socket_db"
            )
            cursor = conn.cursor()
            
            # 1. UPDATE mata pengguna (+1)
            sql_update = "UPDATE user_points SET points = points + 1 WHERE user = %s"
            cursor.execute(sql_update, (client_uid,))
            conn.commit()
            
            # 2. SELECT mata terkini untuk dihantar ke client
            sql_select = "SELECT points FROM user_points WHERE user = %s"
            cursor.execute(sql_select, (client_uid,))
            result = cursor.fetchone()
            
            if result:
                point_str = str(result[0])
            else:
                point_str = "0"
            
            print(f"[SUCCESS] Updated {client_uid}. Current Point: {point_str}", flush=True)
            
            cursor.close()
            conn.close()
            
            # 3. HANTAR point terkini BALIK kepada client
            c.send(point_str.encode())
            print(f"[INFO] Point '{point_str}' dihantar kembali kepada {client_uid}", flush=True)
            
        else:
            print(f"[WARNING] Received empty UID from {addr}", flush=True)
            
    except Exception as e:
        print(f"[ERROR] Transaction failed for {addr}: {e}", flush=True)
    finally:
        c.close()
        print(f"[DISCONNECTED] {addr} closed.", flush=True)

# Main Server Loop
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Supaya port cepat release
s.bind(('0.0.0.0', PORT))
s.listen(10)
print(f"[STARTING] Server listening on port {PORT}...", flush=True)

while True:
    try:
        c, addr = s.accept()
        threading.Thread(target=handle_client, args=(c, addr), daemon=True).start()
    except KeyboardInterrupt:
        print("\n[SHUTDOWN] Server stopping...", flush=True)
        s.close()
        sys.exit()
