#!/usr/bin/make -f
# -*- mode:makefile -*-

all:

clean:
	$(RM) -r /tmp/db
	$(RM) -r /tmp/YoutubeDownloaderApp

run: clean
	$(MAKE) app-workspace
	$(MAKE) run-registry-node &
	sleep 2
	$(MAKE) run-downloads-node &
	sleep 2
	$(MAKE) run-orchestrator-node

run-client-download:
	python3 ./src/client.py --download $1 --Ice.Config=client.config

run-client-transfer:
	python3 ./src/client.py --transfer $1 --Ice.Config=client.config

run-client-list:
	python3 ./src/client.py --Ice.Config=client.config

run-registry-node: /tmp/db/registry /tmp/db/registry-node/servers 
	icegridnode --Ice.Config=registry-node.config

run-orchestrator-node: /tmp/db/orchestrator-node/servers 
	icegridnode --Ice.Config=orchestrator-node.config

run-downloads-node: /tmp/db/downloads-node/servers 
	icegridnode --Ice.Config=downloads-node.config

app-workspace: /tmp/YoutubeDownloaderApp
	cp trawlnet.ice ./src/orchestrator.py ./src/downloader_factory.py \
	./src/transfer_factory.py ./src/utils.py /tmp/YoutubeDownloaderApp
	icepatch2calc /tmp/YoutubeDownloaderApp

/tmp/%:
	mkdir -p $@
