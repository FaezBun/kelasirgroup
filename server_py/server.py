import os, socket, threading, mysql.connector

PORT = int(os.getenv("PORT"))

def handle_client(c):
    try:
        # 1. Terima USER_ID daripada klien
        client_uid = c.recv(1024).decode().strip()
        if client_uid:
            # 2. Update database berdasarkan ID yang klien hantar
            conn = mysql.connector.connect(host="db", user="root", password="rootpassword", database="socket_db")
            cursor = conn.cursor()
            cursor.execute(f"UPDATE user_points SET points = points + 1 WHERE user = '{client_uid}'")
            conn.commit()
            conn.close()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        c.close()

# Main Server Loop
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('0.0.0.0', PORT))
s.listen(5)
print(f"Server listening on port {PORT}...")

while True:
    c, addr = s.accept()
    # 3. Gunakan thread supaya server boleh layan ramai klien serentak
    threading.Thread(target=handle_client, args=(c,), daemon=True).start()
