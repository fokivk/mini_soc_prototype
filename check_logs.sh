#!/bin/bash

# Mini SOC Log Checker Script
# สคริปต์สำหรับดู logs ของระบบ Mini SOC

echo "============================================================"
echo "📊 Mini SOC Log Checker"
echo "🔍 Checking various logs and alerts"
echo "============================================================"

echo ""
echo "🚨 Mini SOC Monitor Logs (Last 20 lines):"
echo "----------------------------------------"
docker logs mini_soc_monitor --tail 20

echo ""
echo "🔍 Suricata Alerts (Last 10 lines):"
echo "-----------------------------------"
if [ -f "alerts/fast.log" ]; then
    tail -10 alerts/fast.log
else
    echo "❌ No fast.log found"
fi

echo ""
echo "📋 Suricata EVE Logs (Last 5 XSS/SQL alerts):"
echo "---------------------------------------------"
if [ -f "alerts/eve.json" ]; then
    grep -i "xss\|sql\|critical" alerts/eve.json | tail -5
else
    echo "❌ No eve.json found"
fi

echo ""
echo "🐳 Docker Container Status:"
echo "---------------------------"
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

echo ""
echo "============================================================"
echo "✅ Log check completed!"
echo "============================================================"
