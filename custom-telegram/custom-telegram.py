#!/usr/bin/env python3
import sys
import json
import urllib.request
import urllib.error

# --- KONFIGURASI ---
BOT_TOKEN = "<isi dengan token bot kalian"
CHAT_ID   = "isikan dengan chat ID kalian"
# --------------------

def get_ip_info(ip):
    """Fitur Nomor 2: Whois Lookup (Negara & ISP)"""
    if ip == "Unknown" or ip == "N/A":
        return "Unknown Location"
    try:
        # Menggunakan API gratis ip-api.com
        with urllib.request.urlopen(f"http://ip-api.com/json/{ip}") as response:
            data = json.loads(response.read().decode())
            if data['status'] == 'success':
                return f"📍 {data['city']}, {data['country']} ({data['isp']})"
    except:
        pass
    return "Lokasi tidak terlacak"

def send_telegram_msg(msg, reply_markup=None):
    """Fungsi kirim pesan dengan dukungan tombol (Fitur Nomor 1)"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": msg,
        "parse_mode": "Markdown",
    }
    if reply_markup:
        payload["reply_markup"] = reply_markup

    json_data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=json_data, headers={'Content-Type': 'application/json'})

    try:
        with urllib.request.urlopen(req) as response:
            pass
    except urllib.error.URLError as e:
        with open('/var/ossec/logs/integrations.log', 'a') as log:
            log.write(f"Telegram Fail: {e.reason}\n")

# --- MAIN LOGIC ---
try:
    alert_file_path = sys.argv[1]
    with open(alert_file_path) as f:
        alert = json.load(f)
except:
    sys.exit(1)

# Ekstrak Data
rule_desc = alert.get('rule', {}).get('description', 'N/A')
level = alert.get('rule', {}).get('level', 0)
agent = alert.get('agent', {}).get('name', 'N/A')
agent_id = alert.get('agent', {}).get('id', 'N/A')
srcip = alert.get('data', {}).get('srcip', alert.get('data', {}).get('src_ip', 'Unknown'))

# Dapatkan info Negara & ISP (Nomor 2)
location_info = get_ip_info(srcip)

# Format Pesan
icon = "🚨" if level >= 10 else "⚠️"
message = f"""
{icon} *SECURITY ALERT DETECTED* {icon}
---------------------------
🔹 *Level*: `{level}`
🔹 *Agent*: `{agent}` (ID: {agent_id})
🔹 *Source IP*: `{srcip}`
🔹 *Info*: `{location_info}`

*Event*:
_{rule_desc}_
---------------------------
*Pilih Tindakan:*
"""

# Buat Tombol Interaktif (Nomor 1)
keyboard = {
    "inline_keyboard": [
        [
            {"text": "🚫 Blokir IP", "callback_data": f"block_{srcip}_{agent_id}"},
            {"text": "🔌 Matikan IoT", "callback_data": f"shutdown_{agent_id}"}
        ],
        [
            {"text": "✅ Abaikan", "callback_data": "ignore"}
        ]
    ]
}

send_telegram_msg(message, reply_markup=keyboard)
sys.exit(0)
