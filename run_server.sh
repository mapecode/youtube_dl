#!/bin/sh
#

echo "Creating directories in /tmp..."
mkdir -p /tmp/YoutubeDownloaderApp
cp trawlnet.ice ./src/orchestrator.py ./src/downloader_factory.py ./src/transfer_factory.py \
./src/utils.py /tmp/YoutubeDownloaderApp
echo "Exec icepatch2calc..."
icepatch2calc /tmp/YoutubeDownloaderApp

echo "Exec registry-node"
mkdir -p /tmp/db/registry
mkdir -p /tmp/db/registry-node/servers
icegridnode --Ice.Config=registry-node.config &
sleep 2

echo "Exec downloads-node"
mkdir -p /tmp/db/downloads-node/servers/distrib/YoutubeDownloaderApp
cp trawlnet.ice ./src/downloader_factory.py ./src/transfer_factory.py ./src/utils.py \
/tmp/db/downloads-node/servers/distrib/YoutubeDownloaderApp
chmod +x /tmp/db/downloads-node/servers/distrib/YoutubeDownloaderApp/*
icegridnode --Ice.Config=downloads-node.config &
sleep 2

echo "Exec orchestrator-node"
mkdir -p /tmp/db/orchestrator-node/servers/distrib/YoutubeDownloaderApp
cp trawlnet.ice ./src/orchestrator.py ./src/utils.py \
/tmp/db/orchestrator-node/servers/distrib/YoutubeDownloaderApp
chmod +x /tmp/db/orchestrator-node/servers/distrib/YoutubeDownloaderApp/*
icegridnode --Ice.Config=orchestrator-node.config

echo "Shoutting down..."
sleep 2
rm $OUT