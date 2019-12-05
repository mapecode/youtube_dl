#!/usr/bin/python3

import sys
import Ice
from color import Color

Ice.loadSlice('trawlnet.ice')
import TrawlNet


class OrchestratorI(TrawlNet.Orchestrator):
    def __init__(self, downloader):
        self.downloader = downloader

    def downloadTask(self, url, current=None):
        if self.downloader is not None:
            return self.downloader.addDownloadTask(url)

    def getFileList(self, current=None):
        pass

    def hello(self, me, current=None):
        pass

    def announce(self, other, current=None):
        pass


class Server(Ice.Application):
    def run(self, argv):
        if len(argv) < 2:
            print(Color.BOLD + Color.RED + 'Error in arguments' + Color.END)
            return -1

        broker = self.communicator()

        downloader_proxy = broker.stringToProxy(argv[1])
        downloader = TrawlNet.DownloaderPrx.checkedCast(downloader_proxy)

        if not downloader:
            raise ValueError(Color.BOLD + Color.RED + 'Invalid proxy ' + Color.END)

        adapter = broker.createObjectAdapter('OrchestratorAdapter')
        servant = OrchestratorI(downloader)
        proxy = adapter.addWithUUID(servant)
        print(proxy, flush=True)
        adapter.activate()

        self.shutdownOnInterrupt()
        broker.waitForShutdown()

        return 0


if __name__ == '__main__':
    sys.exit(Server().main(sys.argv))
