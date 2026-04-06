# 🛡️ IoT SHIELD: Security Gateway & Automated Response

**IoT Shield** adalah sistem keamanan otomatis berbasis *Mini Security Operation Center (SOC)*. Proyek ini dirancang untuk melindungi ekosistem perangkat IoT dari serangan siber seperti **Brute Force** dan **Unauthorized Access**, dengan kemampuan deteksi instan dan mitigasi otomatis di level firewall.

---

## 📑 Daftar Isi

* [Tentang Proyek](#-tentang-proyek)
* [Arsitektur Sistem](#-arsitektur-sistem)
* [Fitur Utama](#-fitur-utama)
* [Prasyarat](#-prasyarat)
* [Panduan Instalasi](#-panduan-instalasi)
* [Metodologi Pengujian](#-metodologi-pengujian)
* [Visualisasi Dashboard](#-visualisasi-dashboard)

---

## 📖 Tentang Proyek

Banyak perangkat IoT masih mengabaikan aspek keamanan dasar. **IoT Shield** hadir sebagai gateway pelindung yang menjembatani jaringan eksternal dengan perangkat IoT lokal.

Dengan menggunakan **Wazuh** sebagai engine analisis log, sistem ini mampu melakukan:

* Deteksi serangan secara real-time
* Respon otomatis terhadap ancaman (*Auto-Recovered Defense*)
* Minim intervensi manual dari administrator

---

## 🏗️ Arsitektur Sistem

Alur kerja sistem:

1. **Detection**
   Monitoring log secara real-time pada IoT Gateway.

2. **Analysis**
   Log dikirim ke Wazuh Manager untuk dianalisis berdasarkan rule-set.

3. **Action**
   Jika terdeteksi serangan, sistem menjalankan *active response* berupa pemblokiran IP menggunakan `iptables`.

4. **Notification**
   Notifikasi instan dikirim ke administrator melalui Telegram.

---

## ✨ Fitur Utama

* ✅ **Real-time Monitoring**
  Pemantauan aktivitas jaringan selama 24/7

* ✅ **Active Response**
  Pemblokiran otomatis IP penyerang menggunakan `iptables`

* ✅ **Telegram SOC**
  Notifikasi dan kontrol keamanan langsung melalui Telegram

* ✅ **Gamified Dashboard**
  Visualisasi serangan dengan tampilan interaktif (laser & hologram)

---

## 🛠️ Prasyarat

Pastikan environment Anda memenuhi kebutuhan berikut:

* **Operating System**: Ubuntu Server 20.04 / 22.04 LTS
* **Tools**: Docker, Docker Compose, Python 3.x
* **Memory**: Minimal 4GB RAM (direkomendasikan untuk Wazuh)

---

## 🚀 Panduan Instalasi

### 1. Clone Repository

```bash
git clone https://github.com/wazuh/wazuh-docker.git -b v4.7.5
cd wazuh-docker/single-node

```

### 2. Deploy SIEM (Wazuh)

```bash
cd wazuh-docker/single-node
docker-compose up -d
```

### 3. Konfigurasi Active Response

Edit file berikut:

```
/wazuh-docker/single-node/config/wazuh_cluster/wazuh_manager.conf

```

Tambahkan konfigurasi:
Verifikasi command firewall-drop
```xml
<command>
  <name>firewall-drop</name>
  <executable>firewall-drop</executable>
  <timeout_allowed>yes</timeout_allowed>
</command>

```

Tambahkan konfigurasi:
Tambahkan blok active response
```xml
<active-response>
  <command>firewall-drop</command>
  <location>local</location>
  <rules_id>5716,5503</rules_id>
  <timeout>60</timeout>
</active-response>
```
Catatan: Kita set timeout 60 detik agar Anda bisa melihat proses blokir dan lepas blokir (unban) secara cepat saat demo.


```

Tambahkan konfigurasi:
White List
```xml
<global>
  <white_list>127.0.0.1</white_list>
  <white_list>localhost</white_list>
  <white_list>172.16.0.0/12</white_list>
  <white_list>192.168.1.1</white_list> </global>
```
Simpan file ctrl + x + y enter

---

## Penerapan Konfigurasi

Agar perubahan di wazuh_manager.conf bisa terbaca, kita perlu merestart container Manager

Jalankan beris perintah berikut :

```
docker restart single-node_wazuh.manager_1

```

## 🧪 Metodologi Pengujian

### 1. Monitor Log pada Agent

```bash
sudo tail -f /var/ossec/logs/active-responses.log
```

### 2. Simulasi Serangan (Fake Brute Force)

Jalankan di terminal terpisah:

```bash
for i in {1..5}; do
  echo "Apr 6 22:00:00 ubuntu-server sshd[9999]: Failed password for root from 192.168.103.250 port 22 ssh2" | sudo tee -a /var/log/auth.log
done
```

### 3. Verifikasi Pemblokiran

```bash
sudo iptables -L -n
```

Pastikan IP penyerang sudah masuk ke daftar blokir.

---

## 📊 Visualisasi Dashboard

<img width="1365" height="632" alt="image" src="https://github.com/user-attachments/assets/1bf33631-8af2-43d3-b55f-4e41a09ac42e" />


Sistem ini menyediakan antarmuka visual interaktif untuk:

* Monitoring serangan secara geografis
* Analisis statistik ancaman
* Visualisasi real-time aktivitas jaringan


Tinggal bilang aja 👍
