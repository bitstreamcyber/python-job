import psutil
import socket

# CPU Usage
cpu = psutil.cpu_percent(interval=1)

# Memory Usage
memory = psutil.virtual_memory()
ram = memory.percent

# Disk Usage
disk = psutil.disk_usage('/')
disk_percent = disk.percent

# IP Address
hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)

print("=== PC HEALTH CHECK ===")
print(f"CPU Usage: {cpu}%")

# CPU Warning
if cpu < 70:
    print("CPU Status: Normal")
elif cpu < 90:
    print("CPU Status: Warning - High CPU usage")
else:
    print("CPU Status: CRITICAL - Very high CPU usage")

print(f"RAM Usage: {ram}%")

# RAM Warning
if ram < 80:
    print("RAM Status: Normal")
elif ram < 90:
    print("RAM Status: Warning - High RAM usage")
else:
    print("RAM Status: CRITICAL - Very high RAM usage")

print(f"Disk Usage: {disk_percent}%")

# Disk Warning
if disk_percent < 85:
    print("Disk Status: Normal")
elif disk_percent < 95:
    print("Disk Status: Warning - Low disk space")
else:
    print("Disk Status: CRITICAL - Disk almost full")

print(f"Hostname: {hostname}")
print(f"IP Address: {ip_address}")

input("Press Enter to exit...")