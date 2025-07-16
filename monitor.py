import psutil
import time
import csv
import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# === CONFIGURATION ===

CSV_FILE = "server_monitoring_log.csv"
SLEEP_INTERVAL = 10  # secondes entre chaque mesure

# Seuils d’alerte (en %)
THRESHOLDS = {
    "cpu": 80,
    "ram": 85,
    "disk": 90,
    "swap": 50,
    "net_sent": 100 * 1024 * 1024,  # 100 MB/s upload
    "net_recv": 100 * 1024 * 1024,  # 100 MB/s download
}

# Configuration email d’alerte
EMAIL_ENABLED = False
SMTP_SERVER = "smtp.example.com"
SMTP_PORT = 587
SMTP_USER = "alert@example.com"
SMTP_PASS = "votre_mot_de_passe"
EMAIL_FROM = "alert@example.com"
EMAIL_TO = "admin@example.com"


# === FONCTIONS ===

def send_email(subject, body):
    if not EMAIL_ENABLED:
        return
    msg = MIMEMultipart()
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.send_message(msg)
        print("[ALERTE] Email envoyé.")
    except Exception as e:
        print(f"[ERREUR] Envoi email impossible : {e}")

def gather_metrics(prev_net_io):
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    swap = psutil.swap_memory()
    net_io = psutil.net_io_counters()

    net_sent = (net_io.bytes_sent - prev_net_io.bytes_sent) / SLEEP_INTERVAL if prev_net_io else 0
    net_recv = (net_io.bytes_recv - prev_net_io.bytes_recv) / SLEEP_INTERVAL if prev_net_io else 0

    metrics = {
        "cpu": cpu,
        "ram": ram.percent,
        "disk": disk.percent,
        "swap": swap.percent,
        "net_sent": net_sent,
        "net_recv": net_recv,
    }
    return metrics, net_io

def check_alerts(metrics):
    alerts = []
    if metrics["cpu"] > THRESHOLDS["cpu"]:
        alerts.append(f"CPU usage élevé : {metrics['cpu']}% > {THRESHOLDS['cpu']}%")
    if metrics["ram"] > THRESHOLDS["ram"]:
        alerts.append(f"RAM usage élevé : {metrics['ram']}% > {THRESHOLDS['ram']}%")
    if metrics["disk"] > THRESHOLDS["disk"]:
        alerts.append(f"Disk usage élevé : {metrics['disk']}% > {THRESHOLDS['disk']}%")
    if metrics["swap"] > THRESHOLDS["swap"]:
        alerts.append(f"Swap usage élevé : {metrics['swap']}% > {THRESHOLDS['swap']}%")
    if metrics["net_sent"] > THRESHOLDS["net_sent"]:
        alerts.append(f"Upload réseau élevé : {metrics['net_sent'] / (1024*1024):.2f} MB/s > {THRESHOLDS['net_sent'] / (1024*1024)} MB/s")
    if metrics["net_recv"] > THRESHOLDS["net_recv"]:
        alerts.append(f"Download réseau élevé : {metrics['net_recv'] / (1024*1024):.2f} MB/s > {THRESHOLDS['net_recv'] / (1024*1024)} MB/s")
    return alerts

def write_csv(timestamp, metrics):
    header = ["timestamp", "cpu", "ram", "disk", "swap", "net_sent_bytes_per_s", "net_recv_bytes_per_s"]
    try:
        with open(CSV_FILE, 'x', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header)
    except FileExistsError:
        pass
    with open(CSV_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            timestamp,
            metrics["cpu"],
            metrics["ram"],
            metrics["disk"],
            metrics["swap"],
            int(metrics["net_sent"]),
            int(metrics["net_recv"]),
        ])

def print_report(timestamp, metrics, alerts):
    print(f"[{timestamp}]")
    print(f"CPU: {metrics['cpu']}% | RAM: {metrics['ram']}% | Disk: {metrics['disk']}% | Swap: {metrics['swap']}%")
    print(f"Net Sent: {metrics['net_sent'] / (1024*1024):.2f} MB/s | Net Recv: {metrics['net_recv'] / (1024*1024):.2f} MB/s")
    if alerts:
        print(">>> ALERTES:")
        for alert in alerts:
            print(f" - {alert}")
    else:
        print("Aucune alerte.")
    print("-" * 60)

# === BOUCLE PRINCIPALE ===

def main():
    prev_net_io = None
    while True:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        metrics, prev_net_io = gather_metrics(prev_net_io)
        alerts = check_alerts(metrics)
        write_csv(timestamp, metrics)
        print_report(timestamp, metrics, alerts)
        if alerts and EMAIL_ENABLED:
            send_email(f"Alertes serveur à {timestamp}", "\n".join(alerts))
        time.sleep(SLEEP_INTERVAL - 1)  # déjà passé 1s dans cpu_percent(interval=1)

if __name__ == "__main__":
    main()
