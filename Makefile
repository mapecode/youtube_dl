#!/usr/bin/make -f
# -*- mode:makefile -*-

all: stop clean
	sh run_server.sh

app-workspace: /tmp/YoutubeDownloaderApp /tmp/DownloadedFiles/
	cp trawlnet.ice ./src/orchestrator.py ./src/downloader_factory.py \
	./src/transfer_factory.py ./src/utils.py /tmp/YoutubeDownloaderApp
	icepatch2calc /tmp/YoutubeDownloaderApp

run-registry-node: /tmp/db/registry /tmp/db/registry-node/servers
	icegridnode --Ice.Config=registry-node.config

run-orchestrator-node: /tmp/db/downloads-node/servers/distrib/YoutubeDownloaderApp
	cp trawlnet.ice ./src/downloader_factory.py ./src/transfer_factory.py ./src/utils.py \
	/tmp/db/downloads-node/servers/distrib/YoutubeDownloaderApp
	chmod 777 /tmp/db/downloads-node/servers/distrib/YoutubeDownloaderApp/*
	icegridnode --Ice.Config=orchestrator-node.config

run-downloads-node: /tmp/db/orchestrator-node/servers/distrib/YoutubeDownloaderApp
	cp trawlnet.ice ./src/orchestrator.py ./src/utils.py \
	/tmp/db/orchestrator-node/servers/distrib/YoutubeDownloaderApp
	chmod 777 /tmp/db/orchestrator-node/servers/distrib/YoutubeDownloaderApp/*
	icegridnode --Ice.Config=downloads-node.config

run-client-download:
	python3 ./src/client.py --download --Ice.Config=client.config

run-client-transfer:
	python3 ./src/client.py --transfer --Ice.Config=client.config

run-client-list:
	python3 ./src/client.py --Ice.Config=client.config

/tmp/%:
	mkdir -p $@

clean:
	$(RM) -r /tmp/db
	$(RM) -r /tmp/YoutubeDownloaderApp

stop:
	killall icegridnode