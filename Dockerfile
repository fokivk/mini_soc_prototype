FROM python:3.9-slim

WORKDIR /app

# ติดตั้ง dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# สร้างโฟลเดอร์สำหรับ scripts
RUN mkdir -p /app/scripts /app/alerts /app/logs

# คัดลอกไฟล์ Python scripts
COPY scripts/ /app/scripts/

# ตั้งค่าสิทธิ์การรัน
RUN chmod +x /app/scripts/*.py

# รัน Python script
CMD ["python", "/app/scripts/main.py"]
