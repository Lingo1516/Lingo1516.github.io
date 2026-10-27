#!/usr/bin/env bash
# OpenClaw 一鍵部署 — 貼到 TAT 終端執行
# 用法: 在 TAT 貼這一行
#   curl -fsSL https://raw.githubusercontent.com/Lingo1516/Lingo1516.github.io/main/openclaw-deploy-tencent.sh | sudo bash -s "ubuntu" "sk-agy-xj002642506513-20260202103284f2f35f648f"
# 或本地執行: sudo bash tencent-deploy.sh ubuntu sk-agy-xj002642506513-20260202103284f2f35f648f
set -euo pipefail

TARGET_USER="${1:-ubuntu}"
AGNES_KEY="${2:-sk-agy-xj002642506513-20260202103284f2f35f648f}"
JIUYAN_KEY="sk-8d9c1452144e1084a4934267b66b95459322957412f487e856103634b591663a"

echo "=== OpenClaw 部署 $(date) 目標用戶: $TARGET_USER ==="

# Node 22
if ! command -v node >/dev/null 2>&1; then
  curl -fsSL https://deb.nodesource.com/setup_22.x | bash -
  apt-get install -y -qq nodejs
fi
echo "node: $(node -v)"

# OpenClaw
npm install -g openclaw@latest
echo "openclaw: $(openclaw --version 2>/dev/null || echo 已裝)"

# 目錄
sudo mkdir -p /home/$TARGET_USER/.openclaw/workspace
sudo chown -R $TARGET_USER:$TARGET_USER /home/$TARGET_USER/.openclaw

# 配置
sudo tee /home/$TARGET_USER/.openclaw/openclaw.json > /dev/null <<CFG
{
  "models": {
    "providers": {
      "agnes": {
        "baseUrl": "https://agnes-sapiens-ai-6e8c3254f46e2f5f-1258972605.ap-southeast-1.vpc.vercel.app",
        "api": "openai-chat",
        "apiKey": "$AGNES_KEY",
        "models": [
          {"id":"agnes-3.0-flash","name":"agnes-3.0-flash","ctx":65536,"cost":{"input":0,"output":0,"cacheRead":0,"cacheWrite":0}}
        ]
      },
      "jiuyan": {
        "baseUrl": "https://ai.jiuyandataapi.com",
        "api": "openai-chat",
        "apiKey": "$JIUYAN_KEY",
        "models": [
          {"id":"deepseek-v4-flash","name":"deepseek-v4-flash","ctx":65536,"cost":{"input":0,"output":0,"cacheRead":0,"cacheWrite":0}}
        ]
      }
    }
  },
  "agents": {
    "defaults": {
      "model": { "primary": "agnes/agnes-3.0-flash", "fallbacks": ["jiuyan/deepseek-v4-flash"] }
    }
  }
}
CFG

# systemd 24h
sudo tee /etc/systemd/system/openclaw.service > /dev/null <<EOF
[Unit]
Description=OpenClaw Gateway (Tencent Lighthouse)
After=network-online.target
Wants=network-online.target

[Service]
User=$TARGET_USER
WorkingDirectory=/home/$TARGET_USER/.openclaw/workspace
Environment="HOME=/home/$TARGET_USER"
ExecStart=$(which openclaw) gateway --port 8443
Restart=always
RestartSec=5
LimitNOFILE=65536

[Install]
WantedBy=multi-user.target
EOF

sudo chown -R $TARGET_USER:$TARGET_USER /home/$TARGET_USER/.openclaw
sudo systemctl daemon-reload
sudo systemctl enable openclaw.service
sudo systemctl restart openclaw.service

sleep 3
echo "=== 部署完成 $(date) ==="
echo "查狀態: sudo journalctl -u openclaw -n 50 --no-pager"
echo "查 OpenClaw: sudo -u $TARGET_USER openclaw status"
