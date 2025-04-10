#!/usr/bin/env bash

# wait-for-it.sh

set -e

TIMEOUT=15
WAITFORIT_CMD="wait-for-it"

while [[ $# -gt 0 ]]; do
  case "\$1" in
    --timeout)
      TIMEOUT="\$2"
      shift 2
      ;;
    --)
      shift
      break
      ;;
    *)
      HOST="\$1"
      PORT="\$2"
      shift 2
      ;;
  esac
done

if [[ -z "$HOST" || -z "$PORT" ]]; then
  echo "Usage: $WAITFORIT_CMD host:port"
  exit 1
fi

echo "Waiting for $HOST:$PORT..."

for i in $(seq $TIMEOUT); do
  nc -z "$HOST" "$PORT" && echo "$HOST:$PORT is available!" && exit 0
  echo "Waiting for $HOST:$PORT..."
  sleep 1
done

echo "Timeout waiting for $HOST:$PORT"
exit 1
