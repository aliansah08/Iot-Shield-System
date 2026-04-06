🛡️ IoT Shield: Cyber Defense Automation & Mini SOC
IoT Shield adalah sistem keamanan otomatis yang dirancang untuk melindungi ekosistem perangkat IoT dari serangan siber seperti Brute Force dan Port Scanning. Sistem ini berfungsi sebagai Mini SOC (Security Operation Center) yang tidak hanya mendeteksi, tapi juga langsung memblokir serangan secara real-time.

🌟 Fitur Utama
Real-Time Detection: Menggunakan Wazuh untuk memantau log sistem dan mendeteksi anomali.

Active Response (Auto-Block): Integrasi otomatis dengan iptables untuk memutus koneksi IP penyerang segera setelah terdeteksi.

Telegram Incident Alert: Bot notifikasi yang mengirimkan detail serangan (IP, Lokasi, Waktu) langsung ke smartphone kamu.

Interactive Visualization: Dashboard monitoring dengan visualisasi animasi laser dan hologram untuk mempermudah pemantauan status keamanan.

🏗️ Arsitektur Sistem
Sistem ini bekerja melalui tiga lapisan pertahanan:

Lapis Infiltrasi (Agent): Perangkat IoT yang dipasang modul pemantau log.

Lapis Analisis (Manager): Server pusat yang menganalisis ancaman menggunakan Ruleset khusus.

Lapis Mitigasi (Automation): Script Python yang mengeksekusi perintah blokir dan mengirim notifikasi.
