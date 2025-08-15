#!/usr/bin/env python3
"""
Mini SOC Alert Monitor
ระบบตรวจจับการโจมตีด้วย Suricata และ Zeek
"""

import os
import time
import json
import logging
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from colorama import init, Fore, Back, Style
import subprocess
import threading

# Initialize colorama for colored output
init(autoreset=True)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/app/logs/mini_soc.log'),
        logging.StreamHandler()
    ]
)

class AlertHandler(FileSystemEventHandler):
    """Handler สำหรับตรวจจับการเปลี่ยนแปลงไฟล์ alert"""
    
    def __init__(self):
        self.last_processed = {}
        self.alert_count = 0
        
    def on_modified(self, event):
        if not event.is_directory:
            self.process_alert_file(event.src_path)
    
    def process_alert_file(self, file_path):
        """ประมวลผลไฟล์ alert"""
        try:
            if file_path.endswith('.json'):
                self.process_suricata_alerts(file_path)
            elif file_path.endswith('.log'):
                self.process_zeek_logs(file_path)
        except Exception as e:
            logging.error(f"Error processing {file_path}: {e}")
    
    def process_suricata_alerts(self, file_path):
        """ประมวลผล alert จาก Suricata"""
        try:
            with open(file_path, 'r') as f:
                for line in f:
                    if line.strip():
                        try:
                            alert = json.loads(line)
                            if alert.get('event_type') == 'alert':
                                self.display_suricata_alert(alert)
                        except json.JSONDecodeError:
                            continue
        except FileNotFoundError:
            pass
    
    def process_zeek_logs(self, file_path):
        """ประมวลผล log จาก Zeek"""
        try:
            # ตรวจสอบว่าเป็นไฟล์ binary หรือ text
            if file_path.endswith('.log'):
                # ตรวจสอบว่าเป็น pcap file หรือไม่
                try:
                    with open(file_path, 'rb') as f:
                        header = f.read(4)
                        # pcap magic number
                        if header in [b'\xa1\xb2\xc3\xd4', b'\xd4\xc3\xb2\xa1']:
                            # เป็น pcap file - ข้ามไป
                            return
                except:
                    pass
                
                # ถ้าไม่ใช่ pcap file ให้อ่านเป็น text
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        for line in f:
                            if line.strip():
                                # ตรวจสอบว่าเป็น log ที่มีข้อมูลการโจมตีหรือไม่
                                if any(keyword in line for keyword in ['XSS Attack', 'SQL Injection Attack', 'HTTP Request']):
                                    self.display_zeek_log(line.strip())
                except UnicodeDecodeError:
                    # ถ้า decode ไม่ได้ ให้ข้ามไป
                    pass
        except FileNotFoundError:
            pass
    
    def display_suricata_alert(self, alert):
        """แสดง Suricata alert"""
        self.alert_count += 1
        
        # ตรวจสอบประเภทการโจมตี
        attack_type = "Unknown"
        color = Fore.WHITE
        
        if "XSS" in alert.get('alert', {}).get('signature', ''):
            attack_type = "XSS Attack"
            color = Fore.RED
        elif "SQL Injection" in alert.get('alert', {}).get('signature', ''):
            attack_type = "SQL Injection Attack"
            color = Fore.MAGENTA
        
        # แสดงผลใน terminal
        print(f"\n{color}{'='*60}")
        print(f"{color}🚨 SURICATA ALERT #{self.alert_count}")
        print(f"{color}{'='*60}")
        print(f"{color}⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{color}🎯 Attack Type: {attack_type}")
        print(f"{color}📝 Signature: {alert.get('alert', {}).get('signature', 'N/A')}")
        print(f"{color}🌐 Source IP: {alert.get('src_ip', 'N/A')}")
        print(f"{color}🎯 Target IP: {alert.get('dest_ip', 'N/A')}")
        print(f"{color}🔗 Protocol: {alert.get('proto', 'N/A')}")
        print(f"{color}📊 Severity: {alert.get('alert', {}).get('severity', 'N/A')}")
        print(f"{color}{'='*60}")
        
        # บันทึก log
        logging.warning(f"Suricata Alert: {attack_type} from {alert.get('src_ip', 'N/A')}")
    
    def display_zeek_log(self, log_line):
        """แสดง Zeek log"""
        if "XSS Attack" in log_line or "SQL Injection Attack" in log_line:
            self.alert_count += 1
            
            attack_type = "XSS Attack" if "XSS" in log_line else "SQL Injection Attack"
            color = Fore.RED if "XSS" in log_line else Fore.MAGENTA
            
            print(f"\n{color}{'='*60}")
            print(f"{color}🔍 ZEEK ALERT #{self.alert_count}")
            print(f"{color}{'='*60}")
            print(f"{color}⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"{color}🎯 Attack Type: {attack_type}")
            print(f"{color}📝 Details: {log_line}")
            print(f"{color}{'='*60}")
            
            logging.warning(f"Zeek Alert: {attack_type} - {log_line}")
        elif "HTTP Request" in log_line:
            # แสดง HTTP requests สำหรับการติดตาม
            print(f"{Fore.BLUE}📡 HTTP Request: {log_line}")

def check_network_interface():
    """ตรวจสอบ network interface"""
    interface = os.getenv('INTERFACE', 'eth0')
    
    try:
        # ใน Docker container อาจไม่มี interface เดียวกัน
        result = subprocess.run(['ip', 'link', 'show'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            if interface in result.stdout:
                print(f"{Fore.GREEN}✅ Network interface {interface} is available")
                return True
            else:
                print(f"{Fore.YELLOW}⚠️  Network interface {interface} not found, but other interfaces available")
                return True  # ยังคงทำงานได้
        else:
            print(f"{Fore.RED}❌ Cannot check network interfaces")
            return False
    except Exception as e:
        print(f"{Fore.RED}❌ Error checking network interface: {e}")
        return False

def start_monitoring():
    """เริ่มการ monitor"""
    print(f"{Fore.CYAN}🚀 Starting Mini SOC Alert Monitor...")
    print(f"{Fore.CYAN}📡 Monitoring interface: {os.getenv('INTERFACE', 'eth0')}")
    print(f"{Fore.CYAN}🐳 Running in Docker container...")
    
    # ตรวจสอบ network interface
    if not check_network_interface():
        print(f"{Fore.YELLOW}⚠️  Warning: Network interface may not be available")
    
    # สร้างโฟลเดอร์สำหรับ logs
    os.makedirs('/app/logs', exist_ok=True)
    os.makedirs('/app/alerts', exist_ok=True)
    
    # เริ่ม file watcher
    event_handler = AlertHandler()
    observer = Observer()
    observer.schedule(event_handler, '/app/alerts', recursive=True)
    observer.start()
    
    print(f"{Fore.GREEN}✅ Monitoring started successfully!")
    print(f"{Fore.CYAN}👀 Watching for alerts in /app/alerts directory...")
    print(f"{Fore.CYAN}📊 Logs will be saved to /app/logs directory...")
    print(f"{Fore.CYAN}🔍 Monitoring Suricata and Zeek alerts...")
    print(f"{Fore.YELLOW}Press Ctrl+C to stop monitoring...")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print(f"\n{Fore.YELLOW}🛑 Stopping Mini SOC Alert Monitor...")
    
    observer.join()

if __name__ == "__main__":
    start_monitoring()
