#!/bin/bash
# OpenClaw 一鍵部署腳本 — 貼到 TAT 終端執行
# 會自動裝 Node 22、OpenClaw、配 model/telegram、設 systemd 24h
set -e

echo "=== OpenClaw 部署開始 ==="

# 1. Node 22
curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
sudo apt-get install -y -qq nodejs
echo "node: $(node -v)"

# 2. OpenClaw
sudo npm install -g openclaw@latest
echo "openclaw: $(openclaw --version 2>/dev/null)"

# 3. 建立目錄
sudo mkdir -p /home/ubuntu/.openclaw/workspace
sudo chown -R ubuntu:ubuntu /home/ubuntu/.openclaw

# 4. 配置（agnes 模型 + telegram）
sudo tee /home/ubuntu/.openclaw/openclaw.json > /dev/null <<'EOF'
{
  "models": {
    "providers": {
      "agnes": {
        "baseUrl": "https://agnes-sapiens-ai-6e8c3254f46e2f5f-1258972605.ap-southeast-1.vpc.vercel.app",
        "api": "openai-chat",
        "apiKey": "sk-agy-xj002642506513-20260202103284f2f35f648f",
        "models": [
          {"id":"agnes-3.0-flash","name":"agnes-3.0-flash"}
        ]
      }
    }
  },
  "channels": {
    "telegram": {
      "enabled": true,
      "botToken": "8817954187:AAFlGvHlVjJ8kqK2ZnLZ9fVjYQz3rTqKc14",
      "dmPolicy": "pairing"
    }
  },
  "agents": {
    "defaults": {
      "model": { "primary": "agnes/agnes-3.0-flash" },
      "heartbeat": {
        "target": "telegram",
        "to": "8966711562"
      }
    }
  }
}
EOF

# 5. systemd 服務（開機自啟 + 24h）
sudo tee /etc/systemd/system/openclaw.service > /dev/null <<EOF
[Unit]
Description=OpenClaw Gateway
After=network-online.target
Wants=network-online.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/.openclaw/workspace
ExecStart=$(which openclaw) gateway --port 8443
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable openclaw.service
sudo systemctl restart openclaw.service

# 6. 驗證
sleep 3
echo "=== 部署完成 ==="
echo "查狀態: sudo journalctl -u openclaw -n 30 --no-pager"
echo "查 openclaw: sudo -u ubuntu openclaw status"
