#!/bin/sh
#

echo "Downloading audio..."
./src/client.py --download --Ice.Config=client.config

echo ""
echo "List request..."
./src/client.py --Ice.Config=client.config

echo ""
echo "Init transfer..."
./src/client.py --transfer --Ice.Config=client.config