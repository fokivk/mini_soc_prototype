#!/bin/bash

# Mini SOC Log Cleaner Script
# สคริปต์สำหรับลบ logs ทั้งหมด

echo "============================================================"
echo "🧹 Mini SOC Log Cleaner"
echo "🗑️  Clearing all logs and restarting services"
echo "============================================================"

echo ""
echo "🛑 Stopping Mini SOC Monitor..."
docker stop mini_soc_monitor
docker rm mini_soc_monitor

echo ""
echo "🗑️  Clearing Suricata logs..."
sudo rm -f alerts/fast.log alerts/eve.json alerts/suricata.log
sudo touch alerts/fast.log alerts/eve.json alerts/suricata.log
sudo chown nanthaphat:nanthaphat alerts/fast.log alerts/eve.json alerts/suricata.log

echo ""
echo "🗑️  Clearing Mini SOC Monitor logs..."
sudo rm -f logs/mini_soc.log
sudo touch logs/mini_soc.log
sudo chown nanthaphat:nanthaphat logs/mini_soc.log

echo ""
echo "🗑️  Clearing Zeek logs..."
sudo rm -f alerts/zeek.log alerts/http_requests.log
sudo touch alerts/zeek.log alerts/http_requests.log
sudo chown nanthaphat:nanthaphat alerts/zeek.log alerts/http_requests.log

echo ""
echo "🔄 Restarting Mini SOC Monitor..."
docker-compose up -d alert_monitor

echo ""
echo "⏳ Waiting for services to start..."
sleep 5

echo ""
echo "✅ Logs cleared and services restarted!"
echo "📊 You can now run tests with: ./run_test.sh"
echo "============================================================"
