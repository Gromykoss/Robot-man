#!/bin/bash
# Robot-man ZaGuu loop poller — каждые 3 мин опрашивает задачи и играет ходы.
# Лог: ~/robot-man/zaaguu/logs/loop.log
cd /home/hermes-workspace/robot-man/zaaguu || exit 1
mkdir -p logs
while true; do
    ts=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    out=$(python3 harness.py loop 2>&1)
    echo "[$ts] $out" >> logs/loop.log
    # Если есть активная игра в фазе, где нужен ход — лог покажет действия
    sleep 180
done
