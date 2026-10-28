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
OC_BIN="$(command -v openclaw || echo /usr/local/bin/openclaw)"
sudo tee /etc/systemd/system/openclaw.service > /dev/null <<EOF
[Unit]
Description=OpenClaw Gateway (Tencent Lighthouse)
After=network-online.target
Wants=network-online.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/.openclaw/workspace
Environment="HOME=/home/ubuntu"
ExecStart=${OC_BIN} gateway --port 8443
Restart=always
RestartSec=5
LimitNOFILE=65536

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable openclaw.service
sudo systemctl restart openclaw.service
sleep 3

# 6. 綁定 Mac 桌面金鑰（讓外部 SSH 直接可用，不用再靠 TAT）
MAC_PUB="ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAICnLLhe60poNJLly1fxT943SRqMkIrZDNYoVOuqXBwBu lingochen@LingodeMacBook-Air.local"
sudo mkdir -p /home/ubuntu/.ssh
sudo grep -qF "$MAC_PUB" /home/ubuntu/.ssh/authorized_keys 2>/dev/null || sudo tee -a /home/ubuntu/.ssh/authorized_keys > /dev/null <<< "$MAC_PUB"
sudo chmod 700 /home/ubuntu/.ssh
sudo chmod 600 /home/ubuntu/.ssh/authorized_keys
echo "=== 金鑰已綁定 ==="

# 7. 驗證
echo "=== 部署完成 $(date) ==="
sudo systemctl status openclaw --no-pager | head -10
echo "log: sudo journalctl -u openclaw -n 30 --no-pager"
