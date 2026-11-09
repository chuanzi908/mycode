#!/bin/bash
# entrypoint.sh — Container entrypoint that starts mock services then hands off.
#
# Usage inside Dockerfile:
#   COPY services/ /opt/services/
#   COPY entrypoint.sh /opt/entrypoint.sh
#   ENTRYPOINT ["/opt/entrypoint.sh"]
#
# Environment:
#   SERVICES       — space-separated list of service names to start (e.g. "gmail contacts kb")
#   FIXTURES_DIR   — path to fixture files inside container (default: /workspace/fixtures)
#
# Each service reads its fixture path from a *_FIXTURES env var.
# e.g. GMAIL_FIXTURES=/workspace/fixtures/gmail/inbox.json

set -euo pipefail

SERVICES="${SERVICES:-}"
FIXTURES_DIR="${FIXTURES_DIR:-/workspace/fixtures}"
SERVICES_DIR="/opt/services"
LOG_DIR="/var/log/services"
mkdir -p "${LOG_DIR}"

if [[ -z "${SERVICES}" ]]; then
    echo "[entrypoint] No SERVICES specified, skipping service startup."
    exec "$@"
fi

# Port map (embedded from port_map.json at build time)
declare -A PORT_MAP=(
    [gmail]=9100 [calendar]=9101 [todo]=9102 [contacts]=9103
    [finance]=9104 [notes]=9105 [kb]=9106 [helpdesk]=9107
    [inventory]=9108 [rss]=9109 [crm]=9110 [config]=9111
    [scheduler]=9112 [web]=9113 [web_real]=9114
    [web_real_injection]=9115 [ocr]=9116 [documents]=9117 [caption]=9118
    [user_agent]=9119
)

PIDS=()

start_service() {
    local name="$1"
    local port="${PORT_MAP[$name]:-}"
    if [[ -z "$port" ]]; then
        echo "[entrypoint] WARNING: unknown service '$name', skipping"
        return
    fi

    local server_py="${SERVICES_DIR}/${name}/server.py"
    if [[ ! -f "$server_py" ]]; then
        echo "[entrypoint] WARNING: $server_py not found, skipping"
        return
    fi

    echo "[entrypoint] Starting ${name} on port ${port}..."
    PORT="$port" python3 "$server_py" \
        > "${LOG_DIR}/${name}.log" 2>&1 &
    PIDS+=($!)
}

health_check() {
    local name="$1"
    local port="${PORT_MAP[$name]:-}"
    local endpoint="http://localhost:${port}"
    local max_wait=15
    local waited=0

    while ((waited < max_wait)); do
        if curl -sf "${endpoint}" >/dev/null 2>&1 || \
           curl -sf -X POST "${endpoint}" >/dev/null 2>&1; then
            echo "[entrypoint] ${name} ready on port ${port}"
            return 0
        fi
        sleep 0.3
        waited=$((waited + 1))
    done
    echo "[entrypoint] WARNING: ${name} did not become ready within ${max_wait}s"
    return 1
}

cleanup() {
    echo "[entrypoint] Shutting down services..."
    for pid in "${PIDS[@]}"; do
        kill "$pid" 2>/dev/null || true
    done
    wait
}
trap cleanup EXIT INT TERM

# Start all requested services
for svc in ${SERVICES}; do
    start_service "$svc"
done

# Wait for all services to be ready
sleep 1
for svc in ${SERVICES}; do
    health_check "$svc" || true
done

echo "[entrypoint] All services started. Executing: $*"
exec "$@"
