Panduan Lengkap: Integrasi Wazuh dengan Bot Telegram Interaktif
Langkah 1: Persiapan Bot Telegram
Sebelum menyentuh server, kamu harus membuat "identitas" bot kamu terlebih dahulu.

Buka aplikasi Telegram dan cari @BotFather.

Ketik /newbot, lalu ikuti instruksinya (beri nama dan username bot).

Simpan API Token yang diberikan (Contoh: 8361916554:AAEIpS...).

Cari bot @userinfobot atau @getmyid_bot, lalu kirim pesan apa saja untuk mendapatkan Chat ID kamu (angka seperti 7919964034).

Cari bot yang baru kamu buat tadi di Telegram, lalu klik Start.

Langkah 2: Membuat Script Integrasi di Wazuh Server (VM 2)
Script ini berfungsi mengirimkan alert dari Wazuh ke Telegram.

Masuk ke terminal VM 2 (Wazuh Server).

Gunakan sudo untuk membuat file di folder integrations:

Bash
sudo nano /root/wazuh-docker/single-node/config/wazuh_cluster/integrations/custom-telegram.py
Masukkan script pengembangan kita (yang sudah ada fitur Whois & Tombol):

Python
#!/usr/bin/env python3
import sys, json, urllib.request, urllib.error

TOKEN = "ISI_TOKEN_KAMU"
CHAT_ID = "ISI_CHAT_ID_KAMU"

def get_ip_info(ip):
    try:
        with urllib.request.urlopen(f"http://ip-api.com/json/{ip}") as response:
            data = json.loads(response.read().decode())
            return f"📍 {data['city']}, {data['country']} ({data['isp']})" if data['status'] == 'success' else "Unknown"
    except: return "Unknown"

# ... (Gunakan sisa script yang sudah saya berikan sebelumnya untuk tombol interaktif)
Wajib: Beri izin akses agar Wazuh bisa menjalankan script ini:

Bash
sudo chmod 750 /root/wazuh-docker/single-node/config/wazuh_cluster/integrations/custom-telegram.py
sudo chown root:wazuh /root/wazuh-docker/single-node/config/wazuh_cluster/integrations/custom-telegram.py
Langkah 3: Mendaftarkan Integrasi di ossec.conf
Wazuh tidak akan tahu ada script baru kalau tidak didaftarkan.

Buka konfigurasi Wazuh Manager (VM 2):

Bash
sudo nano /root/wazuh-docker/single-node/config/wazuh_cluster/manager/etc/ossec.conf
Scroll ke paling bawah (sebelum tag penutup </ossec_config>), lalu tempelkan ini:

XML
<integration>
  <name>custom-telegram.py</name>
  <level>3</level>
  <alert_format>json</alert_format>
</integration>
Restart Wazuh Manager:

Bash
sudo docker exec -it 1670f08eb50c_single-node_wazuh.manager_1 /var/ossec/bin/wazuh-control restart
Langkah 4: Membuat Listener Bot (Penerima Perintah Balik)
Agar tombol "Blokir IP" bekerja, kamu butuh script yang stand-by di VM 2.

Instal library yang dibutuhkan:

Bash
sudo apt update && sudo apt install python3-pip -y
pip3 install python-telegram-bot
Buat file bot_listener.py di folder home kamu:

Bash
nano ~/bot_listener.py
Masukkan kode listener yang saya berikan sebelumnya. Kode ini akan menjalankan perintah agent_control milik Wazuh setiap kali kamu klik tombol di Telegram.

Jalankan: python3 ~/bot_listener.py

Langkah 5: Pengujian (Proof of Concept)
Buka terminal VM 1 (IoT Gateway) atau mesin penyerang (Kali Linux).

Lakukan serangan Hydra:

Bash
hydra -l root -P pass.txt ssh://[IP_VM1] -t 4 -v
Cek HP kamu: Telegram akan mengirim alert lengkap dengan lokasi penyerang dan tombol interaktif.

Klik "Blokir IP": Periksa di VM 1 dengan sudo iptables -L, IP tersebut seharusnya sudah terblokir.
