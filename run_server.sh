#!/bin/sh
#

echo "Creating directories in /tmp..."
mkdir -p /tmp/YoutubeDownloaderApp
cp trawlnet.ice orchestrator.py downloader_factory.py transfer_factory.py \
utils.py /tmp/YoutubeDownloaderApp
echo "Exec icepatch2calc..."
icepatch2calc /tmp/YoutubeDownloaderApp

echo "Exec registry-node"
mkdir -p /tmp/db/registry
mkdir -p /tmp/db/registry-node/servers
icegridnode --Ice.Config=registry-node.config &
sleep 2

echo "Exec downloads-node"
mkdir -p /tmp/db/downloads-node/servers
icegridnode --Ice.Config=downloads-node.config &
sleep 2

echo "Exec orchestrator-node"
mkdir -p /tmp/db/orchestrator-node/servers
icegridnode --Ice.Config=orchestrator-node.config

echo "Shoutting down..."
sleep 2
rm $OUT