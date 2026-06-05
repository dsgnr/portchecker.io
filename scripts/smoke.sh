#!/usr/bin/env bash
#
# Compose-level smoke test:
# - builds the prod images from this checkout
# - brings the stack up
# - hits the API and the nginx proxy
# - tears everything down unless KEEP_STACK=1
#
# Used by CI (.github/workflows/pr-stack.yml) and locally.
#
# Usage:
#   scripts/smoke.sh
#   KEEP_STACK=1 scripts/smoke.sh

set -Eeuo pipefail
shopt -s inherit_errexit 2>/dev/null || true

readonly ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
readonly COMPOSE_FILE="${ROOT_DIR}/docker-compose.smoke.yml"
readonly WEB_URL="http://127.0.0.1:8080"
readonly API_URL="http://127.0.0.1:8000"

log() {
  printf '%s\n' "$*"
}

group_begin() {
  printf '::group::%s\n' "$*"
}

group_end() {
  printf '::endgroup::\n'
}

fail() {
  printf 'SMOKE FAIL: %s\n' "$*" >&2
  exit 1
}

require_cmd() {
  command -v "$1" >/dev/null 2>&1 || fail "missing required command: $1"
}

compose() {
  docker compose -f "$COMPOSE_FILE" "$@"
}

http_get() {
  curl -fsS "$1"
}

http_status() {
  curl -s -o /dev/null -w '%{http_code}' "$1"
}

http_post_json() {
  local url="$1"
  local payload="$2"
  curl -fsS -X POST -H 'Content-Type: application/json' -d "$payload" "$url"
}

expect_eq() {
  local expected="$1"
  local actual="$2"
  local context="$3"

  [[ "$actual" == "$expected" ]] || fail "$context expected '$expected', got: $actual"
}

expect_contains() {
  local haystack="$1"
  local needle="$2"
  local context="$3"

  grep -Fq "$needle" <<<"$haystack" || fail "$context missing '$needle'"
}

cleanup() {
  local status="$1"

  if [[ "${KEEP_STACK:-0}" == "1" ]]; then
    log "KEEP_STACK=1 set, leaving stack running."
    exit "$status"
  fi

  if (( status != 0 )); then
    group_begin "Compose logs"
    compose logs --no-color || true
    group_end
  fi

  compose down -v --remove-orphans >/dev/null 2>&1 || true
  exit "$status"
}

trap 'cleanup $?' EXIT

require_cmd docker
require_cmd curl
require_cmd grep

cd "$ROOT_DIR"

group_begin "docker compose build"
compose build --no-cache
group_end

group_begin "docker compose up"
compose up -d --wait --wait-timeout 120
group_end

log "==> GET /healthz (direct)"
body="$(http_get "${API_URL}/healthz")"
expect_eq "true" "$body" "/healthz"

log "==> GET /api/me with do-connecting-ip header"
body="$(curl -fsS -H 'do-connecting-ip: 203.0.113.7' "${API_URL}/api/me")"
expect_eq "203.0.113.7" "$body" "/api/me"

log "==> GET /api/{host}/{port} with explicit host (port-target sidecar)"
body="$(http_get "${API_URL}/api/port-target/9999")"
expect_eq "True" "$body" "/api/port-target/9999"

log "==> GET /api/{host}/{port} closed port"
body="$(http_get "${API_URL}/api/port-target/9998")"
expect_eq "False" "$body" "/api/port-target/9998"

log "==> POST /api/query (mixed open/closed)"
body="$(http_post_json "${API_URL}/api/query" '{"host":"port-target","ports":[9999,9998]}')"
log "    body: $body"
expect_contains "$body" '"port":9999' "POST /api/query"
expect_contains "$body" '"port":9998' "POST /api/query"
expect_contains "$body" '"error":false' "POST /api/query"
expect_contains "$body" '"host":"port-target"' "POST /api/query"

log "==> POST /api/query (invalid port -> 400)"
status="$(curl -s -o /dev/null -w '%{http_code}' \
  -X POST -H 'content-type: application/json' \
  -d '{"host":"port-target","ports":[70000]}' \
  "${API_URL}/api/query")"
expect_eq "400" "$status" "POST /api/query invalid port"

log "==> GET /docs"
status="$(http_status "${API_URL}/docs")"
expect_eq "200" "$status" "/docs"

log "==> GET /metrics"
status="$(http_status "${API_URL}/metrics")"
expect_eq "200" "$status" "/metrics"

log "==> GET / (nginx)"
body="$(http_get "${WEB_URL}/")"
expect_contains "$body" 'id="form"' "index.html"
expect_contains "$body" 'id="host"' "index.html"
expect_contains "$body" 'id="ports"' "index.html"

log "==> nginx proxies /api/* to the api service"
body="$(http_get "${WEB_URL}/api/port-target/9999")"
expect_eq "True" "$body" "proxied /api/port-target/9999"

log "==> nginx proxies /docs"
status="$(http_status "${WEB_URL}/docs")"
expect_eq "200" "$status" "proxied /docs"

log
log "SMOKE PASS"