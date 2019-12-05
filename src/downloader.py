#!/usr/bin/python3

import sys
import Ice
from color import Color
from download_mp3 import download_mp3

Ice.loadSlice('trawlnet.ice')
import TrawlNet


class DownloaderI(TrawlNet.Downloader):
    def addDownloadTask(self, url, current=None):
        print(url)
        sys.stdout.flush()
        return download_mp3(url)

    def newFile(self):
        pass




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


if __name__ == '__main__':
    sys.exit(Server().main(sys.argv))
