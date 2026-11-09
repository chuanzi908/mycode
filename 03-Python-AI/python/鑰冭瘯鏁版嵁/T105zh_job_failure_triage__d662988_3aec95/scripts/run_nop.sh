#!/bin/bash
set -e
TASK_DIR="$(cd "$(dirname "$0")/.." && pwd)"
TASK_NAME=$(basename "$TASK_DIR")

echo "=== Building Docker image ==="
docker build -t test-${TASK_NAME} -f ${TASK_DIR}/environment/Dockerfile ${TASK_DIR}/environment/ 2>/dev/null

echo "=== Running Nop test (no solution, should get reward=0) ==="
docker run --rm \
  -v ${TASK_DIR}/tests:/tests \
  test-${TASK_NAME} \
  bash -c "mkdir -p /logs/verifier /app/output && \
           bash /tests/test.sh && \
           echo '---' && echo 'REWARD:' && cat /logs/verifier/reward.txt"
