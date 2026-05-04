# 📡 Integrasi Wazuh dengan Bot Telegram (Interactive Alerting)

Dokumentasi ini menjelaskan cara mengintegrasikan **Wazuh SIEM** dengan **Bot Telegram** untuk mengirim alert secara real-time, lengkap dengan fitur interaktif seperti *IP lookup* dan *blokir IP langsung dari Telegram*.

---

## 📌 Arsitektur

* **VM 1** → IoT Gateway / Target (yang diserang)
* **VM 2** → Wazuh Server (Manager + Integration + Bot Listener)
* **Telegram Bot** → Media notifikasi & kontrol

---

## 🚀 Fitur

* 🔔 Alert real-time dari Wazuh ke Telegram
* 🌍 Informasi lokasi IP (GeoIP / Whois)
* 🛑 Tombol interaktif untuk blokir IP
* ⚡ Otomatisasi response dari Telegram ke Wazuh

---

## 1️⃣ Persiapan Bot Telegram

### Buat Bot

1. Buka Telegram → cari `@BotFather`

2. Jalankan:

   ```
   /newbot
   ```

3. Ikuti instruksi:

   * Nama bot
   * Username bot

4. Simpan **API Token**

   ```
   contoh: 123456789:AAxxxxxxxxxxxxxxxx
   ```

---

### Ambil Chat ID

1. Cari bot:

   * `@userinfobot` atau `@getmyid_bot`
2. Kirim pesan apa saja
3. Simpan **Chat ID**

---

### Aktivasi Bot

* Cari bot yang sudah dibuat → klik **Start**

---

## 2️⃣ Setup Script Integrasi di Wazuh Server

Script ini berfungsi mengirim alert dari Wazuh ke Telegram.

### 📂 Lokasi File

```bash
sudo nano /root/wazuh-docker/single-node/config/wazuh_cluster/integrations/custom-telegram.py
```

---

### ⚠️ Best Practice (WAJIB)

Jangan hardcode token di dalam script. Gunakan environment variable:

```bash
export TELEGRAM_TOKEN="ISI_TOKEN_KAMU"
export TELEGRAM_CHAT_ID="ISI_CHAT_ID_KAMU"
```

---

### 🧠 Script Integrasi

File: `custom-telegram.py`

```python
#!/usr/bin/env python3
import os, sys, json, urllib.request

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def get_ip_info(ip):
    try:
        with urllib.request.urlopen(f"http://ip-api.com/json/{ip}") as response:
            data = json.loads(response.read().decode())
            if data['status'] == 'success':
                return f"{data['city']}, {data['country']} ({data['isp']})"
    except:
        pass
    return "Unknown"

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = json.dumps({
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }).encode()

    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
    urllib.request.urlopen(req)

def main():
    alert_file = sys.argv[1]

    with open(alert_file) as f:
        alert = json.load(f)

    srcip = alert.get("data", {}).get("srcip", "N/A")
    location = get_ip_info(srcip)

    message = f"""
🚨 *Wazuh Alert*
IP: `{srcip}`
Lokasi: {location}
Rule: {alert.get("rule", {}).get("description", "-")}
"""

    send_telegram(message)

if __name__ == "__main__":
    main()
```

---

### 🔐 Permission

```bash
sudo chmod 750 /root/wazuh-docker/single-node/config/wazuh_cluster/integrations/custom-telegram.py
sudo chown root:wazuh /root/wazuh-docker/single-node/config/wazuh_cluster/integrations/custom-telegram.py
```

---

## 3️⃣ Registrasi Integrasi di Wazuh

Edit file konfigurasi:

```bash
sudo nano /root/wazuh-docker/single-node/config/wazuh_cluster/manager/etc/ossec.conf
```

Tambahkan sebelum `</ossec_config>`:

```xml
<integration>
  <name>custom-telegram.py</name>
  <level>3</level>
  <alert_format>json</alert_format>
</integration>
```

---

### 🔁 Restart Wazuh Manager

Cek container:

```bash
sudo docker ps
```

Restart:

```bash
sudo docker exec -it <container_name> /var/ossec/bin/wazuh-control restart
```

---

## 4️⃣ Setup Bot Listener (Interactive Command)

Agar tombol seperti **"Blokir IP"** bisa digunakan.

---

### Install Dependency

```bash
sudo apt update
sudo apt install python3-pip -y
pip3 install python-telegram-bot
```

---

### Buat Listener

```bash
nano ~/bot_listener.py
```

> Isi script listener sesuai implementasi interactive command (blokir IP, dll).

---

### Jalankan Listener

```bash
python3 ~/bot_listener.py
```

---

### 💡 (Opsional - Production)

Gunakan systemd agar bot berjalan otomatis:

```bash
sudo nano /etc/systemd/system/telegram-bot.service
```

---

## 5️⃣ Pengujian (Proof of Concept)

### Simulasi Serangan

```bash
hydra -l root -P pass.txt ssh://[IP_VM1] -t 4 -v
```

---

### Hasil yang Diharapkan

* 📲 Telegram menerima alert
* 🌍 Menampilkan lokasi attacker
* 🔘 Tombol interaktif muncul
* 🛑 Klik “Blokir IP” → IP terblokir

---

### Verifikasi

```bash
sudo iptables -L
```

---

## ⚠️ Catatan Keamanan

* Jangan commit token ke GitHub
* Gunakan environment variable atau `.env`
* Validasi input sebelum eksekusi command
* Batasi akses ke Wazuh Manager

---

## 📌 Improvement

* Integrasi dengan active response Wazuh
* Logging command dari Telegram
* Multi-user control (RBAC)
* Dashboard monitoring

---

## 🎯 Kesimpulan

Integrasi ini memungkinkan:

* Monitoring real-time
* Response cepat dari Telegram
* Automasi keamanan berbasis alert

---
