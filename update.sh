#!/bin/sh
# dockmaster 一键更新:拉取最新代码并重建容器
[ -f config.json ] || { echo "首次运行:先 cp config.example.json config.json"; exit 1; }
set -e
cd "$(dirname "$0")"
echo "== dockmaster 更新 =="
git pull --ff-only
sudo -n /usr/local/bin/docker compose up -d --build
echo "== 完成 =="
sudo -n /usr/local/bin/docker ps --filter name=13002-dockmaster --format "{{.Names}} {{.Status}}"
