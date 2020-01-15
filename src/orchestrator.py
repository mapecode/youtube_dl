#!/usr/bin/python3
# pylint: disable=C0114
import sys
import Ice
# pylint: disable=E0401
from utils import Color, generate_id, supported, get_topic, get_topic_manager, DOWNLOADER_TOPIC_NAME, ORCHESTRATOR_TOPIC_NAME

Ice.loadSlice('trawlnet.ice')
# pylint: disable=C0413
import TrawlNet


class OrchestratorI(TrawlNet.Orchestrator):
    """
    Orchestrator interface implementation for send download request to downloader, generate
    downloaded files list and announce the orchestrator
    """

    def __init__(self, orchestrator):
        """
        @param orchestrator: orchestrator service
        """
        self.orchestrator = orchestrator

    # pylint: disable=C0103, W0613
    def downloadTask(self, url, current=None):
        """
        Create a new download task that will send to a downloader if the file does not exist
        already in the system.
        @param url: link to the video
        @param current:
        @return: download request result
        """
        return self.orchestrator.send_download_task(url)

    def getFileList(self, current=None):
        """
        Provides the list of available files (already downloaded and indexed) of all
        system downloaders.
        @param current:
        @return: the files info
        """
        return self.orchestrator.get_files()

    def announce(self, other, current=None):
        """
        Announce an orchestrator when there is a new orchestrator in the system.
        @param other: an orchestrator
        @param current:
        @return:
        """
        self.orchestrator.new_orchestrator(other)


class OrchestratorEventI(TrawlNet.OrchestratorEvent):
    # pylint: disable=R0903
    """
    OrchestratorEvent interface implementation for report the existence of a new orchestrator
    """

    def __init__(self, orchestrator):
        """
        @param orchestrator: orchestrator service
        """
        self.orchestrator = orchestrator

    # pylint: disable=C0103, W0613
    def hello(self, me, current=None):
        """
        Reports orchestrators that already exist in the system that it is a new orchestrator.
        @param me: an orchestrator
        @param current:
        @return:
        """
        self.orchestrator.hello_to(me)


class UpdateEventI(TrawlNet.UpdateEvent):
    # pylint: disable=R0903
    """
    UpdateEvent interface implementation for update the list of files
    """

    def __init__(self, orchestrator):
        """
        @param orchestrator: orchestrator service
        """
        self.orchestrator = orchestrator

    # pylint: disable=C0103, W0613
    def newFile(self, file, current=None):
        """
        Reports orchestrators that there is a new file in the system.
        @param file: downloaded file
        @param current:
        @return:
        """
        self.orchestrator.files_dic[file.hash] = file.name


class Orchestrator:
    """
    Orchestrator service implementation
    """

    def __init__(self, broker, downloader_prx):
        """
        @param broker: for orchestrator adapter
        @param downloader_prx: downloader proxy
        """
        self.orchestrators_dic = {}  # Orchestrators Dictionary {key = proxy, value = broker}
        self.files_dic = {}  # Files Dictionary {key = file_hash, value = file_name}

        # self.adapter = broker.createObjectAdapter('OrchestratorAdapter')
        # self.downloader = TrawlNet.DownloaderPrx.checkedCast(broker.stringToProxy(downloader_prx))

        #if not self.downloader:
        #    raise ValueError(Color.BOLD + Color.RED + 'Invalid proxy ' + Color.END)

        self.adapter = broker.createObjectAdapter('OrchestratorAdapter')
        properties = self.adapter.getProperties()

        # Get downloader factory

        transfer_factory_prx = properties.getProperty('TransferFactory')
        transfer_factory_proxy = broker.stringToProxy(transfer_factory_prx)
        transfer_factory = TrawlNet.TransferFactoryPrx.checkedCast(transfer_factory_proxy)

        if not transfer_factory:
            raise ValueError('Invalid proxy for TransferFactory')

        # Topic manager preguntar tobias

        # Get topics with my_storm
        topic_manager = get_topic_manager(broker)
        self.topic_orchestrator = get_topic(
            topic_manager, ORCHESTRATOR_TOPIC_NAME)
        self.topic_updates = get_topic(
            topic_manager, DOWNLOADER_TOPIC_NAME)

        # Orchestrator subscriber event
        sync_subscriber = OrchestratorEventI(self)
        self.sync_subscriber_prx = self.adapter.addWithUUID(sync_subscriber)  # proxy
        self.topic_orchestrator.subscribeAndGetPublisher({}, self.sync_subscriber_prx)

        # Orchestrator publisher event
        self.publisher = TrawlNet.OrchestratorEventPrx.uncheckedCast(
            self.topic_orchestrator.getPublisher())

        # Updates Event subscriber
        updates_subscriber = UpdateEventI(self)
        self.updates_subscriber_prx = self.adapter.addWithUUID(updates_subscriber)  # proxy
        self.topic_updates.subscribeAndGetPublisher({}, self.updates_subscriber_prx)

        # Orchestrator servant
        servant = OrchestratorI(self)
        self.servant_prx = self.adapter.addWithUUID(servant)  # proxy

    def start(self):
        """
        Start the orchestrator service
        @return:
        """
        self.adapter.activate()
        self.publisher.hello(TrawlNet.OrchestratorPrx.checkedCast(self.servant_prx))

    def stop(self):
        """
        Stop the orchestrator service
        @return:
        """
        self.topic_orchestrator.unsubscribe(self.sync_subscriber_prx)
        self.topic_updates.unsubscribe(self.updates_subscriber_prx)

    def send_download_task(self, url):
        """
        Send an download request
        @param url: link to video
        @return: the information file
        """
        if not supported(url):
            raise ValueError(Color.RED + 'Incorrect URL' + Color.END)

        file_id = generate_id(url)
        if file_id not in self.files_dic:
            try:
                return self.downloader.addDownloadTask(url)
            except TrawlNet.DownloadError as msg_exception:
                raise msg_exception
        else:
            file = TrawlNet.FileInfo()
            file.hash = file_id
            file.name = self.files_dic[file_id] + " (Downloaded previously)"
            return file

    def hello_to(self, orchestrator):
        """
        Notify the rest of the orchestrators that there is a new orchestrator
        @param orchestrator:
        @return:
        """
        orchestrator_str = orchestrator.ice_toString()
        if orchestrator_str not in self.orchestrators_dic:
            print("New orchestrator: " + str(orchestrator_str))
            self.orchestrators_dic[orchestrator_str] = orchestrator
            orchestrator.announce(TrawlNet.OrchestratorPrx.checkedCast(self.servant_prx))

    def new_orchestrator(self, orchestrator):
        """
        Notify who the previous orchestrator is
        @param orchestrator:
        @return:
        """
        orchestrator_str = orchestrator.ice_toString()
        if orchestrator_str not in self.orchestrators_dic:
            print("Previous orchestrator: " + str(orchestrator_str))
            self.orchestrators_dic[orchestrator_str] = orchestrator

    def get_files(self):
        """
        Get the list of files already downloaded
        @return: the list
        """
        files = []
        for file_id in self.files_dic:
            file = TrawlNet.FileInfo()
            file.hash = file_id
            file.name = self.files_dic[file_id]
            files.append(file)
        return files


class Server(Ice.Application):
    """
    Orchestrator server
    """

    def run(self, args):
        """
        Run implementation
        @param args: execution arguments
        @return: success execution
        """
        if len(args) < 2:
            ValueError(Color.BOLD + Color.RED + 'Error in arguments' + Color.END)

        broker = self.communicator()
        orchestrator = Orchestrator(broker, args[1])
        orchestrator.start()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()
        orchestrator.stop()

        return 0


if __name__ == '__main__':
    sys.exit(Server().main(sys.argv))
