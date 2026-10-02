#!/usr/bin/env bash
# ビルド済み target/ROOT.war を Tomcat ($CATALINA_HOME) にデプロイして (再)起動する。
#   ./scripts/deploy.sh          # デプロイのみ
#   ./scripts/deploy.sh --build  # mvn -q clean package してからデプロイ
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
CATALINA_HOME="${CATALINA_HOME:-/opt/tomcat}"
CATALINA_BASE="${CATALINA_BASE:-$CATALINA_HOME}"
export CATALINA_HOME CATALINA_BASE

if [[ "${1:-}" == "--build" ]]; then
  (cd "$PROJECT_DIR" && mvn -q clean package)
fi

# CATALINA_BASE が未作成なら CATALINA_HOME の conf をコピーして初期化
if [[ ! -f "$CATALINA_BASE/conf/server.xml" ]]; then
  echo "[deploy] initialize CATALINA_BASE: $CATALINA_BASE"
  mkdir -p "$CATALINA_BASE"/{conf,logs,temp,webapps,work}
  cp -r "$CATALINA_HOME"/conf/* "$CATALINA_BASE/conf/"
fi

# 停止 (起動していなければ無視)
if pgrep -f "catalina.base=$CATALINA_BASE" >/dev/null; then
  echo "[deploy] stop tomcat"
  "$CATALINA_HOME/bin/shutdown.sh" >/dev/null 2>&1 || true
  for _ in $(seq 1 30); do pgrep -f "catalina.base=$CATALINA_BASE" >/dev/null || break; sleep 1; done
  pkill -9 -f "catalina.base=$CATALINA_BASE" 2>/dev/null || true
fi

# 古いアプリを削除して配置
rm -rf "$CATALINA_BASE/webapps/ROOT" "$CATALINA_BASE/webapps/ROOT.war" "$CATALINA_BASE/work/Catalina"
cp "$PROJECT_DIR/target/ROOT.war" "$CATALINA_BASE/webapps/ROOT.war"

echo "[deploy] start tomcat"
"$CATALINA_HOME/bin/startup.sh" >/dev/null

# 起動待ち
for _ in $(seq 1 90); do
  code=$(curl -s -o /dev/null -w '%{http_code}' http://localhost:8080/login || true)
  if [[ "$code" == "200" ]]; then
    echo "[deploy] OK: http://localhost:8080/login"
    exit 0
  fi
  sleep 2
done
echo "[deploy] NG: /login did not return 200. see $CATALINA_BASE/logs/catalina.out" >&2
tail -50 "$CATALINA_BASE/logs/catalina.out" >&2 || true
exit 1
