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
git clone https://github.com/username/iot-shield.git
cd iot-shield
```

### 2. Deploy SIEM (Wazuh)

```bash
cd wazuh-docker/single-node
docker-compose up -d
```

### 3. Konfigurasi Active Response

Edit file berikut:

```
/var/ossec/etc/ossec.conf
```

Tambahkan konfigurasi:

```xml
<active-response>
  <command>firewall-drop</command>
  <location>local</location>
  <rules_id>5716</rules_id>
</active-response>
```

---

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

> Tambahkan screenshot dashboard Anda di sini

Sistem ini menyediakan antarmuka visual interaktif untuk:

* Monitoring serangan secara geografis
* Analisis statistik ancaman
* Visualisasi real-time aktivitas jaringan


Tinggal bilang aja 👍
