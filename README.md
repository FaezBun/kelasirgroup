# Multi-Language Socket Communication and Horizontal Scaling in a Dockerized Infrastructure

This project demonstrates high-performance socket communication between different programming languages (C and Python) within a horizontally scalable Docker environment. 
*(Projek ini mendemonstrasikan komunikasi socket berprestasi tinggi antara pelbagai bahasa pengaturcaraan (C dan Python) di dalam persekitaran Docker yang sedia untuk digandakan / horizontal scaling).*

## 🚀 Features
* **Multi-Language Sockets:** Real-time raw data exchange between C and Python using TCP/UDP Sockets.
* **Horizontal Scaling:** Easily scale up containerized servers and clients to handle higher loads.
* **Dockerized:** Fully isolated services within a secure internal network (`socket_net`).
* **Cloudflare Tunnel:** Securely expose the local dashboard to the internet without port forwarding.

## 🏗️ Architecture
* **Dashboard:** Streamlit application (Python) for the user interface.
* **Database:** MySQL 8.0 for robust data logging.
* **Backend:** Scalable C and Python socket servers/clients.

---

## 🌐 Alternative: Local Access (Without Cloudflare Tunnel)

If you prefer not to use Cloudflare Tunnel, you can bypass it entirely. Simply open your web browser and access the Dashboard directly using your server's IP address and port `8501`:
👉 **`http://<your-server-ip>:8501`** (e.g., `http://192.168.1.50:8501`)

*(Jika anda tidak mahu menggunakan Cloudflare Tunnel, anda boleh terus membuka Dashboard melalui web browser menggunakan IP server anda dan port 8501: `http://<ip-server-anda>:8501`)*

---

## ⚙️ Cloudflare Tunnel Setup (Subdomain Configuration)

To expose the Dashboard to your own custom subdomain (e.g., `supra.yourdomain.com`), you **must** insert your Cloudflare Tunnel Token into the `docker-compose.yml` file.

*(Untuk memaparkan Dashboard ke subdomain anda sendiri secara live, anda **wajib** memasukkan Cloudflare Tunnel Token anda ke dalam fail `docker-compose.yml`.)*

1. Open `docker-compose.yml`.
2. Locate the `tunnel` service block.
3. Replace `YOUR_CLOUDFLARE_TOKEN` with your actual token from the Cloudflare Zero Trust Dashboard.

```yaml
  tunnel:
    image: cloudflare/cloudflared:latest
    restart: unless-stopped
    network_mode: "host" 
    environment:
      - TUNNEL_TOKEN=YOUR_CLOUDFLARE_TOKEN
    command: tunnel --no-autoupdate run
