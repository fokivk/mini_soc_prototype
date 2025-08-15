# Mini SOC Prototype

ระบบตรวจจับการโจมตีแบบ mini SOC ที่ใช้ Suricata และ Zeek ในการตรวจจับ XSS และ SQL Injection



## การติดตั้ง
```bash
# ติดตั้ง Docker และ Docker Compose
sudo apt update
sudo apt install docker.io docker-compose

# เริ่ม Docker service
sudo systemctl start docker
sudo systemctl enable docker

# เพิ่ม user เข้า docker group (optional)
sudo usermod -aG docker $USER

# ติดตั้ง Python dependencies (สำหรับ local testing)
pip install -r requirements.txt
```

## การใช้งาน
```bash
# เริ่มระบบทั้งหมด
python3 scripts/start_system.py

# หรือเริ่มด้วย Docker Compose โดยตรง
docker-compose up -d

# ทดสอบการโจมตี (ในอีก terminal)
python3 scripts/test_attacks.py

# ดู logs
docker-compose logs -f

# ดูสถานะ services
docker-compose ps

# หยุดระบบ
docker-compose down
```

## โครงสร้างไฟล์
- `scripts/`: โฟลเดอร์สำหรับ Python scripts
  - `main.py`: ไฟล์หลักสำหรับรันระบบ monitor
  - `test_attacks.py`: สคริปต์ทดสอบการโจมตี
  - `start_system.py`: สคริปต์เริ่มระบบทั้งหมด
- `suricata_config/`: คอนฟิก Suricata
  - `suricata.yaml`: ไฟล์คอนฟิกหลัก
  - `rules/custom.rules`: กฎการตรวจจับ XSS และ SQL Injection
- `zeek_config/`: คอนฟิก Zeek
  - `local.zeek`: ไฟล์คอนฟิกสำหรับตรวจจับการโจมตี
- `alerts/`: ไฟล์ alert จาก Suricata และ Zeek
- `logs/`: ไฟล์ logs ของระบบ
- `docker-compose.yml`: สำหรับรันระบบทั้งหมดด้วย Docker
- `Dockerfile`: สำหรับสร้าง Python alert monitor container

## ระบบที่ใช้
- **Suricata**: IDS/IPS สำหรับตรวจจับการโจมตี
- **Zeek**: Network Security Monitor
- **DVWA**: Web application สำหรับทดสอบการโจมตี
- **MySQL**: Database สำหรับ DVWA
- **Python**: แสดงผล alert ใน terminal
- **Docker**: Containerization platform

## การทำงาน
1. **Suricata** จะ monitor network traffic บน interface wlan0
2. **Zeek** จะ analyze network protocols และตรวจจับการโจมตี
3. **Python Monitor** จะ watch ไฟล์ logs และแสดง alert ใน terminal
4. **DVWA** จะเป็น target สำหรับทดสอบการโจมตี
5. เมื่อมีการโจมตี ระบบจะแสดง alert พร้อมรายละเอียด

## การทดสอบ
1. เริ่มระบบด้วย `python3 scripts/start_system.py`
2. รอให้ระบบเริ่มต้นเสร็จ (ประมาณ 1-2 นาที)
3. เปิด browser ไปที่ `http://localhost:8080` เพื่อเข้าถึง DVWA
4. รัน `python3 scripts/test_attacks.py` เพื่อทดสอบการโจมตี
5. ดู alert ใน terminal ที่รัน main.py

## หมายเหตุ
- ระบบนี้ใช้สำหรับการศึกษาและทดสอบเท่านั้น
- อย่าใช้บนระบบ production หรือระบบที่ไม่ได้อนุญาต
- ตรวจสอบให้แน่ใจว่า Docker และ Docker Compose ติดตั้งแล้ว
- ระบบจะใช้ network interface wlan0 ในการ monitor
