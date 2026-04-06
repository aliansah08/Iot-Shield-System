🛡️ IoT SHIELD: Security Gateway & Automated Response
IoT Shield adalah sistem keamanan otomatis berbasis Mini Security Operation Center (SOC). Proyek ini dirancang untuk melindungi ekosistem perangkat IoT dari serangan siber seperti Brute Force dan Unauthorized Access dengan melakukan deteksi instan dan mitigasi otomatis pada level firewall.

📑 Daftar Isi
Tentang Proyek

Arsitektur Sistem

Fitur Utama

Prasyarat

Panduan Instalasi

Metodologi Pengujian

Visualisasi Dashbord

📖 Tentang Proyek
Banyak perangkat IoT mengabaikan aspek keamanan dasar. IoT Shield hadir sebagai gateway pelindung yang menjembatani jaringan luar dengan perangkat IoT lokal. Menggunakan Wazuh sebagai otak analisis log, sistem ini mampu "memukul balik" penyerang secara otomatis tanpa intervensi manusia (Auto-Recovered Defense).

🏗️ Arsitektur Sistem
Sistem bekerja dengan alur sebagai berikut:

Detection: Monitoring log secara real-time di sisi IoT Gateway.

Analysis: Log dikirim ke Wazuh Manager untuk dianalisa berdasarkan rule-set.

Action: Jika serangan terdeteksi, Manager memerintahkan Agent untuk menjalankan active-response (Block IP via iptables).

Notification: Notifikasi instan dikirim ke administrator melalui Telegram.

✨ Fitur Utama
✅ Real-time Monitoring: Pantau aktivitas jaringan 24/7.

✅ Active Response: Pemblokiran otomatis IP penyerang menggunakan iptables.

✅ Telegram SOC: Kontrol dan notifikasi keamanan langsung di tangan Anda.

✅ Gamified Dashboard: Visualisasi serangan dengan animasi laser dan hologram interaktif.

🛠️ Prasyarat
Sebelum memulai, pastikan lingkungan Anda memenuhi syarat:

Operating System: Ubuntu Server 20.04/22.04 LTS.

Tools: Docker & Docker Compose, Python 3.x.

Memory: Minimal 4GB RAM (Direkomendasikan untuk kestabilan Wazuh).

🚀 Panduan Instalasi
1. Klon Repositori
Bash
git clone https://github.com/username/iot-shield.git
cd iot-shield
2. Deploy SIEM (Wazuh)
Gunakan Docker untuk instalasi cepat:

Bash
cd wazuh-docker/single-node
docker-compose up -d
3. Konfigurasi Active Response
Edit file /var/ossec/etc/ossec.conf dan tambahkan konfigurasi perintah blokir:

XML
<active-response>
  <command>firewall-drop</command>
  <location>local</location>
  <rules_id>5716</rules_id>
</active-response>
🧪 Metodologi Pengujian
Untuk memastikan sistem bekerja, lakukan simulasi serangan Brute Force palsu:

Monitor Log di Agent:

Bash
sudo tail -f /var/ossec/logs/active-responses.log
Jalankan Serangan (Terminal Terpisah):

Bash
for i in {1..5}; do
  echo "Apr 6 22:00:00 ubuntu-server sshd[9999]: Failed password for root from 192.168.103.250 port 22 ssh2" | sudo tee -a /var/log/auth.log
done
Verifikasi Block:
Cek apakah IP penyerang sudah masuk ke iptables:

Bash
sudo iptables -L -n
📊 Visualisasi Dashboard
(Tambahkan screenshot dashboard hologram kamu di sini)
Sistem ini menyediakan antarmuka visual yang memudahkan pemantauan titik serangan secara geografis dan statistikal.
