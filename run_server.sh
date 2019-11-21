#!/bin/sh

python3 src/downloader.py --Ice.Config=server.config > /tmp/downloader-proxy.out &
PID=$!

sleep 2

python3 src/orchestrator.py --Ice.Config=server.config "$(head -1 /tmp/downloader-proxy.out)" | tee /tmp/orchestrator-proxy.out

kill -KILL $PID