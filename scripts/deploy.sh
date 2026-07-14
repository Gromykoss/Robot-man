#!/usr/bin/env bash
# Robot-man — Deploy Script
# Правила: бэкап → diff → линт → smoke.
set -euo pipefail

DIR="/home/hermes-workspace/robot-man"
BACKUP_TS=$(date +%m%d_%H%M)

red()  { echo -e "\033[31m✗ $*\033[0m"; }
green(){ echo -e "\033[32m✓ $*\033[0m"; }
info() { echo -e "\033[36m→ $*\033[0m"; }

info "=== Robot-man Deploy — $(date '+%Y-%m-%d %H:%M:%S') ==="

cd "$DIR"

# 1. Проверка git
if ! git diff-index --quiet HEAD -- 2>/dev/null; then
    red "Есть незакоммиченные изменения. Сначала git commit."
    exit 1
fi

# 2. Бэкап
info "Бэкап..."
for f in engage.py analytics.py reply_to_comments.py follow_tracked_authors.py; do
    [ -f "$f" ] && cp "$f" "$f.bak.$BACKUP_TS"
done
green "Бэкап готов"

# 3. Линт
info "Линт..."
for f in engage.py analytics.py reply_to_comments.py; do
    python3 -c "import py_compile; py_compile.compile('$f', doraise=True)" 2>/dev/null && \
        green "  $f OK" || red "  $f ОШИБКА"
done

# 4. xurl auth
info "xurl auth..."
xurl whoami >/dev/null 2>&1 && green "xurl auth OK" || red "xurl auth ОШИБКА"

# 5. Smoke
info "Smoke..."
bash ~/.hermes/scripts/robotman-smoke-monitor.sh && green "Smoke ПРОЙДЕН" || red "Smoke ПРОВАЛЕН"

green "=== Деплой завершён ==="
