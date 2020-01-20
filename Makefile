#!/usr/bin/make -f
# -*- mode:makefile -*-

all:
	sh run_server.sh

app-workspace:
	mkdir -p /tmp/YoutubeDownloaderApp
	mkdir -p /tmp/DownloadedFiles
	cp trawlnet.ice ./src/orchestrator.py ./src/downloader_factory.py \
	./src/transfer_factory.py ./src/utils.py /tmp/YoutubeDownloaderApp
	icepatch2calc /tmp/YoutubeDownloaderApp

run-registry-node:
	mkdir -p /tmp/db/registry
	mkdir -p /tmp/db/registry-node/servers
	icegridnode --Ice.Config=registry-node.config

run-downloads-node:
	mkdir -p /tmp/db/downloads-node/servers/distrib/YoutubeDownloaderApp
	cp trawlnet.ice ./src/downloader_factory.py ./src/transfer_factory.py ./src/utils.py \
	/tmp/db/downloads-node/servers/distrib/YoutubeDownloaderApp
	chmod +x /tmp/db/downloads-node/servers/distrib/YoutubeDownloaderApp/*
	icegridnode --Ice.Config=downloads-node.config

run-orchestrator-node:
	mkdir -p /tmp/db/orchestrator-node/servers/distrib/YoutubeDownloaderApp
	cp trawlnet.ice ./src/orchestrator.py ./src/utils.py \
	/tmp/db/orchestrator-node/servers/distrib/YoutubeDownloaderApp
	chmod +x /tmp/db/orchestrator-node/servers/distrib/YoutubeDownloaderApp/*
	icegridnode --Ice.Config=orchestrator-node.config

run-client-download:
	python3 ./src/client.py "OrchestratorServer1 -t -e 1.1 @ Orchestrator1.OrchestratorAdapter" \
	--download --Ice.Config=client.config

run-client-transfer:
	python3 ./src/client.py "OrchestratorServer2 -t -e 1.1 @ Orchestrator2.OrchestratorAdapter" \
	--transfer --Ice.Config=client.config

run-client-list:
	python3 ./src/client.py "OrchestratorServer3 -t -e 1.1 @ Orchestrator3.OrchestratorAdapter" \
	--Ice.Config=client.config

clean:
	$(RM) -r /tmp/db
	$(RM) -r /tmp/YoutubeDownloaderApp
	$(RM) -r /tmp/DownloadedFiles

stop:
	./kill_pids.sh icegridnode