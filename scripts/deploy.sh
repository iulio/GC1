#!/usr/bin/env bash
set -euo pipefail

ENV_FILE="${1:-.deploy.env}"

if [[ ! -f "$ENV_FILE" ]]; then
  echo "Missing $ENV_FILE. Copy .deploy.env.example to .deploy.env and fill in the server details." >&2
  exit 1
fi

set -a
source "$ENV_FILE"
set +a

: "${SSH_HOST:?Missing SSH_HOST}"
: "${SSH_USER:?Missing SSH_USER}"
: "${SSH_PORT:?Missing SSH_PORT}"
: "${REMOTE_PATH:?Missing REMOTE_PATH}"
: "${SSH_KEY:?Missing SSH_KEY}"

if [[ ! -f "$SSH_KEY" ]]; then
  echo "SSH private key not found: $SSH_KEY" >&2
  exit 1
fi

PACKAGE="deploy-package.zip"
rm -f "$PACKAGE"
zip -r "$PACKAGE" passenger_wsgi.py public README.md

SSH_TARGET="${SSH_USER}@${SSH_HOST}"
SSH_ARGS=(-i "$SSH_KEY" -p "$SSH_PORT" -o IdentitiesOnly=yes -o BatchMode=yes)
SCP_ARGS=(-i "$SSH_KEY" -P "$SSH_PORT" -o IdentitiesOnly=yes -o BatchMode=yes)

scp "${SCP_ARGS[@]}" "$PACKAGE" "${SSH_TARGET}:/tmp/global-consult-release.zip"
ssh "${SSH_ARGS[@]}" "$SSH_TARGET" "set -e
mkdir -p '$REMOTE_PATH'
unzip -o /tmp/global-consult-release.zip -d '$REMOTE_PATH'
mkdir -p '$REMOTE_PATH/tmp'
touch '$REMOTE_PATH/tmp/restart.txt'
rm -f /tmp/global-consult-release.zip"

echo "Deployed to ${SSH_HOST}:${REMOTE_PATH}"
