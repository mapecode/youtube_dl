#!/bin/sh

python3 src/client.py "$(head -1 /tmp/orchestrator-proxy.out)" "url"
