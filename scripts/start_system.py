#!/usr/bin/env python3
"""
Start System Script
สคริปต์สำหรับเริ่มระบบ Mini SOC ทั้งหมด
"""

import subprocess
import time
import os
import sys
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

def run_command(command, description):
    """รันคำสั่งและแสดงผล"""
    print(f"{Fore.CYAN}🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"{Fore.GREEN}✅ {description} completed successfully")
            return True
        else:
            print(f"{Fore.RED}❌ {description} failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"{Fore.RED}❌ Error in {description}: {e}")
        return False

def check_docker():
    """ตรวจสอบว่า Docker ติดตั้งแล้วหรือไม่"""
    print(f"{Fore.YELLOW}🔍 Checking Docker installation...")
    try:
        result = subprocess.run(['docker', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"{Fore.GREEN}✅ Docker is installed: {result.stdout.strip()}")
            return True
        else:
            print(f"{Fore.RED}❌ Docker is not installed")
            return False
    except FileNotFoundError:
        print(f"{Fore.RED}❌ Docker is not installed")
        return False

def check_docker_compose():
    """ตรวจสอบว่า Docker Compose ติดตั้งแล้วหรือไม่"""
    print(f"{Fore.YELLOW}🔍 Checking Docker Compose installation...")
    try:
        result = subprocess.run(['docker-compose', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"{Fore.GREEN}✅ Docker Compose is installed: {result.stdout.strip()}")
            return True
        else:
            print(f"{Fore.RED}❌ Docker Compose is not installed")
            return False
    except FileNotFoundError:
        print(f"{Fore.RED}❌ Docker Compose is not installed")
        return False

def start_docker_services():
    """เริ่ม Docker services"""
    print(f"{Fore.CYAN}🚀 Starting Docker services...")
    
    # เปลี่ยนไปยังโฟลเดอร์โปรเจค
    project_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(os.path.dirname(project_dir))
    
    # รัน docker-compose
    if run_command("docker-compose up -d", "Starting Docker services"):
        print(f"{Fore.GREEN}✅ Docker services started successfully!")
        return True
    else:
        print(f"{Fore.RED}❌ Failed to start Docker services")
        return False

def check_services_status():
    """ตรวจสอบสถานะของ services"""
    print(f"{Fore.YELLOW}🔍 Checking services status...")
    
    services = ['mini_soc_suricata', 'mini_soc_zeek', 'mini_soc_mysql', 'mini_soc_webapp', 'mini_soc_monitor']
    
    for service in services:
        try:
            result = subprocess.run(['docker', 'ps', '--filter', f'name={service}', '--format', 'table {{.Names}}\t{{.Status}}'], 
                                  capture_output=True, text=True)
            if service in result.stdout:
                print(f"{Fore.GREEN}✅ {service} is running")
            else:
                print(f"{Fore.RED}❌ {service} is not running")
        except Exception as e:
            print(f"{Fore.RED}❌ Error checking {service}: {e}")

def show_logs():
    """แสดง logs ของ services"""
    print(f"{Fore.CYAN}📊 Showing service logs...")
    
    services = ['mini_soc_suricata', 'mini_soc_zeek', 'mini_soc_mysql', 'mini_soc_monitor']
    
    for service in services:
        print(f"{Fore.YELLOW}📋 Logs for {service}:")
        try:
            result = subprocess.run(['docker', 'logs', '--tail', '10', service], 
                                  capture_output=True, text=True)
            if result.stdout:
                print(result.stdout)
            else:
                print(f"{Fore.GRAY}No logs available")
        except Exception as e:
            print(f"{Fore.RED}❌ Error getting logs for {service}: {e}")
        print()

def main():
    """ฟังก์ชันหลัก"""
    print(f"{Fore.CYAN}{'='*60}")
    print(f"{Fore.CYAN}🚀 Mini SOC System Startup")
    print(f"{Fore.CYAN}{'='*60}")
    
    # ตรวจสอบ Docker
    if not check_docker():
        print(f"{Fore.RED}❌ Please install Docker first")
        sys.exit(1)
    
    # ตรวจสอบ Docker Compose
    if not check_docker_compose():
        print(f"{Fore.RED}❌ Please install Docker Compose first")
        sys.exit(1)
    
    print()
    
    # เริ่ม Docker services
    if start_docker_services():
        print()
        
        # รอให้ services เริ่มต้น
        print(f"{Fore.YELLOW}⏳ Waiting for services to start...")
        time.sleep(15)  # รอนานขึ้นเพื่อให้ MySQL และ webapp เริ่มต้น
        
        # ตรวจสอบสถานะ
        check_services_status()
        print()
        
        # แสดง logs
        show_logs()
        
        print(f"{Fore.GREEN}{'='*60}")
        print(f"{Fore.GREEN}✅ Mini SOC system is ready!")
        print(f"{Fore.GREEN}🌐 Web application: http://localhost:8080")
        print(f"{Fore.GREEN}📊 Monitor logs: Check ./logs directory")
        print(f"{Fore.GREEN}🧪 Test attacks: python3 scripts/test_attacks.py")
        print(f"{Fore.GREEN}🐳 Docker services: docker-compose ps")
        print(f"{Fore.GREEN}📋 View logs: docker-compose logs -f")
        print(f"{Fore.GREEN}{'='*60}")
        
    else:
        print(f"{Fore.RED}❌ Failed to start Mini SOC system")
        sys.exit(1)

if __name__ == "__main__":
    main()
