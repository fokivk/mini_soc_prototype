# Mini SOC Shell Scripts

ไฟล์ shell scripts สำหรับจัดการระบบ Mini SOC

## 📁 ไฟล์ที่มี

### 1. `run_test.sh` - ทดสอบระบบ
```bash
./run_test.sh
```
- ตรวจสอบและสร้าง virtual environment ถ้าจำเป็น
- ติดตั้ง packages ที่จำเป็น (requests, colorama)
- รัน `container_test.py` เพื่อทดสอบ XSS, SQL Injection, Command Injection
- แสดงผลการทดสอบ

### 2. `check_logs.sh` - ดู logs
```bash
./check_logs.sh
```
- แสดง Mini SOC Monitor logs (20 บรรทัดล่าสุด)
- แสดง Suricata alerts (10 บรรทัดล่าสุด)
- แสดง XSS/SQL alerts จาก eve.json (5 บรรทัดล่าสุด)
- แสดงสถานะ Docker containers

### 3. `clear_logs.sh` - ลบ logs ทั้งหมด
```bash
./clear_logs.sh
```
- หยุดและลบ Mini SOC Monitor container
- ลบ Suricata logs (fast.log, eve.json, suricata.log)
- ลบ Mini SOC Monitor logs (mini_soc.log)
- ลบ Zeek logs (zeek.log, http_requests.log)
- รีสตาร์ท Mini SOC Monitor
- สร้างไฟล์ logs ใหม่ที่ว่างเปล่า

## 🚀 วิธีการใช้งาน

### ทดสอบระบบใหม่
```bash
# ลบ logs เก่า
./clear_logs.sh

# ทดสอบระบบ
./run_test.sh

# ดูผลลัพธ์
./check_logs.sh
```

### ดู logs ปัจจุบัน
```bash
./check_logs.sh
```

### ลบ logs เก่า
```bash
./clear_logs.sh
```

## 📊 ผลลัพธ์ที่คาดหวัง

หลังจากรัน `./run_test.sh` คุณควรเห็น:
- XSS Attack alerts
- SQL Injection alerts
- Command Injection alerts

ใน Mini SOC Monitor logs และ Suricata logs

## 🔧 การแก้ไขปัญหา

### ถ้า virtual environment ไม่มี
```bash
python3 -m venv venv
source venv/bin/activate
pip install requests colorama
```

### ถ้า Docker containers ไม่ทำงาน
```bash
docker-compose up -d
```

### ถ้า logs ยังเก่า
```bash
./clear_logs.sh
```
