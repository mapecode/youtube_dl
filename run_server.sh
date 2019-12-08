#!/bin/sh

PYTHON=python3

DOWNLOADER_CONFIG=server.config
ORCHESTRATOR_CONFIG=$DOWNLOADER_CONFIG

PRX=$(tempfile)
$PYTHON downloader.py --Ice.Config=$DOWNLOADER_CONFIG>$PRX &
PID=$!

# Dejamos arrancar al downloader
sleep 1
echo "Downloader: $(cat $PRX)"

# Lanzamos el orchestrator
$PYTHON orchestrator.py --Ice.Config=$ORCHESTRATOR_CONFIG "$(cat $PRX)"

echo "Shoutting down..."
kill -KILL $PID
rm $PRX
