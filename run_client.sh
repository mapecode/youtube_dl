#!/bin/sh
#

echo "Downloading audio..."
./src/client.py --download <url> \
--Ice.Config=client.config

echo ""
echo "List request..."
./src/client.py --Ice.Config=client.config

echo ""
echo "Init transfer..."
./src/client.py --transfer <file_name> \
--Ice.Config=client.config