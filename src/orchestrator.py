#!/usr/bin/python3
import sys
import Ice
from color import Color
import my_storm as my_storm

Ice.loadSlice('trawlnet.ice')
import TrawlNet


class OrchestratorI(TrawlNet.Orchestrator):
    def __init__(self, orchestrator):
        self.orchestrator = orchestrator

    def downloadTask(self, url, current=None):
        return self.orchestrator.send_download_task(url)

    def getFileList(self, current=None):
        return self.orchestrator.get_files()

    def announce(self, other, current=None):
        return self.orchestrator.new_orchestrator(other)


class OrchestratorEventI(TrawlNet.OrchestratorEvent):
    def __init__(self, orchestrator):
        self.orchestrator = orchestrator

    def hello(self, me, current=None):
        self.orchestrator.hello_to(me)


class UpdateEventI(TrawlNet.UpdateEvent):
    def __init__(self, orchestrator):
        self.orchestrator = orchestrator

    def newFile(self, file, current=None):
        self.orchestrator.files_dic[file.hash] = file.name


class Orchestrator:
    def __init__(self, broker, downloader_prx):
        self.orchestrators_dic = {}  # Orchestrators Dictionary {key = proxy, value = broker}
        self.files_dic = {}  # Files Dictionary {key = file_hash, value = file_name}

        self.adapter = broker.createObjectAdapter('OrchestratorAdapter')
        self.downloader = TrawlNet.DownloaderPrx.checkedCast(broker.stringToProxy(downloader_prx))

        if self.downloader is None:
            raise ValueError(Color.BOLD + Color.RED + 'Invalid proxy ' + Color.END)

        # Get topics with my_storm
        topic_manager = my_storm.get_topic_manager(broker)
        self.topic_orchestrator = my_storm.get_topic(topic_manager, my_storm.ORCHESTRATOR_TOPIC_NAME)
        self.topic_updates = my_storm.get_topic(topic_manager, my_storm.DOWNLOADER_TOPIC_NAME)

        # Orchestrator subscriber event
        self.sync_subscriber = OrchestratorEventI(self)
        self.sync_subscriber_prx = self.adapter.addWithUUID(self.sync_subscriber)  # proxy
        self.topic_orchestrator.subscribeAndGetPublisher({}, self.sync_subscriber_prx)

        # Orchestrator publisher event
        self.publisher = TrawlNet.OrchestratorEventPrx.uncheckedCast(self.topic_orchestrator.getPublisher())

        # Updates Event subscriber
        self.updates_subscriber = UpdateEventI(self)
        self.updates_subscriber_prx = self.adapter.addWithUUID(self.updates_subscriber)  # proxy
        self.topic_updates.subscribeAndGetPublisher({}, self.updates_subscriber_prx)

        # Orchestrator servant
        self.servant = OrchestratorI(self)
        self.servant_prx = self.adapter.addWithUUID(self.servant)  # proxy

    def start(self):
        self.adapter.activate()
        self.publisher.hello(TrawlNet.OrchestratorPrx.checkedCast(self.servant_prx))

    def stop(self):
        self.topic.unsubscribe(self.subscriber_prx)

    def send_download_task(self, url):
        return self.downloader.addDownloadTask(url)

    def hello_to(self, orchestrator):
        orchestrator_str = orchestrator.ice_toString()
        if orchestrator_str not in self.orchestrators_dic:
            print("New orchestrator: " + str(orchestrator_str))
            self.orchestrators_dic[orchestrator_str] = orchestrator
            orchestrator.announce(TrawlNet.OrchestratorPrx.checkedCast(self.servant_prx))

    def new_orchestrator(self, orchestrator):
        orchestrator_str = orchestrator.ice_toString()
        if orchestrator_str not in self.orchestrators_dic:
            print("Previous orchestrator: " + str(orchestrator_str))
            self.orchestrators_dic[orchestrator_str] = orchestrator

    def get_files(self):
        for file_hash in self.files_dic:
            file = TrawlNet.FileInfo()
            file.hash = file_hash
            file.name = self.files_dic[file_hash]


"""Server de fase 1
class Server(Ice.Application):
    def run(self, argv):
        if len(argv) < 2:
            ValueError(Color.BOLD + Color.RED + 'Error in arguments' + Color.END)

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
"""


class Server(Ice.Application):
    def run(self, argv):
        if len(argv) < 2:
            ValueError(Color.BOLD + Color.RED + 'Error in arguments' + Color.END)

        broker = self.communicator()
        orchestrator = Orchestrator(broker, argv[1])
        orchestrator.start()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()
        orchestrator.stop()

        return 0


if __name__ == '__main__':
    sys.exit(Server().main(sys.argv))
