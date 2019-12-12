#!/usr/bin/python3

import sys
import os
import hashlib
import Ice
from download_mp3 import download_mp3_with_id
import my_storm as my_storm

Ice.loadSlice('trawlnet.ice')
import TrawlNet


class DownloaderI(TrawlNet.Downloader):
    def __init__(self, publisher):
        self.publisher = publisher

    # Add download task 
    def addDownloadTask(self, url, current=None):
        try:
            out_file, file_id = download_mp3_with_id(url)
        except Exception as e:
            raise TrawlNet.DownloadError(str(e))

        file = TrawlNet.FileInfo()
        file.name = os.path.basename(out_file)
        file.hash = file_id

        self.publisher.newFile(file)

        return file


class Server(Ice.Application):
    def run(self, argv):
        broker = self.communicator()
        adapter = broker.createObjectAdapter("DownloaderAdapter")

        # Get topic manager from my_storm
        topic_manager = my_storm.get_topic_manager(broker)

        # Get topic name from my_storm
        sync_topic = my_storm.get_topic(topic_manager, my_storm.DOWNLOADER_TOPIC_NAME)

        # Downloader Servant
        publisher = TrawlNet.UpdateEventPrx.uncheckedCast(sync_topic.getPublisher())
        servant = DownloaderI(publisher)

        proxy = adapter.addWithUUID(servant)
        print(str(proxy))
        sys.stdout.flush()

        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()

        return 0


if __name__ == '__main__':
    sys.exit(Server().main(sys.argv))

    # Server Fase 1
"""
    class Server(Ice.Application):
        def run(self, argv):
            broker = self.communicator()
            servant = DownloaderI()

            adapter = broker.createObjectAdapter("DownloaderAdapter")
            proxy = adapter.addWithUUID(servant)

            print(proxy, flush=True)

            adapter.activate()
            self.shutdownOnInterrupt()
            broker.waitForShutdown()

            return 0
"""
