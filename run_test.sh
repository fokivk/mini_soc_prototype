#!/bin/bash

# Mini SOC Test Script
# สคริปต์สำหรับทดสอบระบบ Mini SOC

echo "============================================================"
echo "🚀 Mini SOC Test Script"
echo "📡 Testing XSS, SQL Injection, and Command Injection attacks"
echo "============================================================"

# ตรวจสอบว่า virtual environment มีอยู่หรือไม่
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Creating..."
    python3 -m venv venv
    source venv/bin/activate
    pip install requests colorama
    echo "✅ Virtual environment created and packages installed"
else
    echo "✅ Virtual environment found"
fi

# เปิดใช้งาน virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# ตรวจสอบว่า container_test.py มีอยู่หรือไม่
if [ ! -f "scripts/container_test.py" ]; then
    echo "❌ container_test.py not found!"
    exit 1
fi

echo "🧪 Running container test..."
echo "📊 This will send XSS and SQL Injection attacks to test the system"
echo ""

# รัน test
python3 scripts/container_test.py

echo ""
echo "============================================================"
echo "✅ Test completed!"
echo "📊 Check Mini SOC Monitor logs for alerts:"
echo "   docker logs mini_soc_monitor"
echo "============================================================"
