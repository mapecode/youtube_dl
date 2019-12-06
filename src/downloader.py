#!/usr/bin/python3

import sys
import os
import hashlib
import Ice
from src.color import Color
from src.download_mp3 import download_mp3
import src.my_storm as my_storm

Ice.loadSlice('trawlnet.ice')
import TrawlNet


def encode(s):
    h = hashlib.md5(s.encode())
    return h.hexdigest()


class DownloaderI(TrawlNet.Downloader, files_list):
    def __init__(self):
        self.publisher = None

    # Add download task 
    def addDownloadTask(self, url, current=None):
        print("Download request: %s .\n", str(url))
        sys.stdout.flush()
        try:
            exit_file = download_mp3(url)
        except:
            raise Exception()

        print("Downloaded file: %s.\n", str(exit_file))
        sys.stdout.flush()

        file_info = TrawlNet.FileInfo()
        file_info.name = os.path.basename(exit_file)
        file_info.hash = encode(file_info.name)

        ## if self.publisher is not None:
        self.publisher.newFile(file_info)

        return file_info


class Server(Ice.Application):
    def run(self, argv):
        broker = self.communicator()
        adapter = broker.createObjectAdapter("DownloaderAdapter")

        # Get topic manager from my_storm
        sync_topic = my_storm.get_topic_manager(broker)
        if not sync_topic:
            raise ValueError(Color.BOLD + Color.RED + "Invalid proxy in topic manager" + Color.END)

        # Get topic name from my_storm
        try:
            sync_topic = sync_topic.retrieve(my_storm.DOWNLOADER_TOPIC_NAME)
        except my_storm.EXCEPTION:
            print(Color.BOLD + Color.RED + str(my_storm.DOWNLOADER_TOPIC_NAME) + "not found. Creating..." + Color.END)
            sync_topic = sync_topic.create(my_storm.DOWNLOADER_TOPIC_NAME)

        # Downloader Servant
        servant = DownloaderI()
        servant.publisher = TrawlNet.UpdateEventPrx.uncheckedCast(sync_topic.getPublisher())

        proxy = adapter.addWithUUID(servant)
        print(Color.BOLD + Color.GREEN + str(proxy) + Color.END)
        sys.stdout.flush()

        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()

        # End
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