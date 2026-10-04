#!/bin/sh
# dockmaster 一键更新:从 GitHub 拉取最新源码包并重建容器(无需 git)
set -e
cd "$(dirname "$0")"
[ -f config.json ] || { echo "首次运行:先 cp config.example.json config.json"; exit 1; }
echo "== dockmaster 更新 =="
curl -sL --max-time 90 -x http://192.168.31.77:7890 \
  -o /tmp/dockmaster-main.tar.gz \
  https://github.com/mao0824/dockmaster/archive/refs/heads/main.tar.gz
tar -xzf /tmp/dockmaster-main.tar.gz -C /tmp
cp /tmp/dockmaster-main/app.py /tmp/dockmaster-main/index.html /tmp/dockmaster-main/compose.yaml .
sudo -n /usr/local/bin/docker compose up -d --build
rm -rf /tmp/dockmaster-main /tmp/dockmaster-main.tar.gz
echo "== 完成 =="
sudo -n /usr/local/bin/docker ps --filter name=13002-dockmaster --format "{{.Names}} {{.Status}}"
