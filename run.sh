#!/bin/sh

python3 src/downloader.py --Ice.Config=server.config | tee /tmp/downloader-proxy.out

sleep .5
echo "Downloader: $(cat /tmp/downloader-proxy.out)"

python3 src/orchestrator.py --Ice.Config=server.config "$(head -1 /tmp/downloader-proxy.out) " | tee /tmp/orchestrator-proxy.out
echo "Orchestrator: $(cat /tmp/orchestrator-proxy.out)"


python3 src/client.py "$(head -1 /tmp/orchestrator-proxy.out)"
