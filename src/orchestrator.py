#!/usr/bin/python3
"""Dudas
¿Como se manejan varios orchestrators?
¿Cada vez que se crea un orchestrator se crea la estructura de datos que los contiene?
¿El cliente como se conecta con un orchestrator si hay varios lanzados?
¿Cual es la secuencia de pasos que se deben seguir al ejecutar un orchestrator?
¿Los orchestrators son publicadores y suscriptores de ambos canales?
¿Por que las clases de los eventos tienen que tener asociadas un orchestrator?
¿Es correcta la asociacion del orchestrator a una clase de evento pasando la instancia del
orchestrator al crear el evento?
"""
import sys
import Ice
from src.color import Color
import src.my_storm as my_storm

Ice.loadSlice('trawlnet.ice')
import TrawlNet


class OrchestratorI(TrawlNet.Orchestrator):
    def __init__(self, orchestrator, downloader):
        self.orchestrator = orchestrator
        self.downloader = downloader

    def downloadTask(self, url, current=None):
        if self.downloader is not None:
            return self.downloader.addDownloadTask(url)

    def getFileList(self, current=None):
        raise NotImplementedError()

    def announce(self, other, current=None):
        raise NotImplementedError()


class OrchestratorEventI(TrawlNet.OrchestratorEvent):
    def __init__(self, orchestrator):
        self.orchestrator = orchestrator

    def hello(self, me, current=None):
        raise NotImplementedError()


class UpdateEventI(TrawlNet.UpdateEvent):
    def __init__(self, orchestrator):
        self.orchestrator = orchestrator

    def newFile(self, file, current=None):
        raise NotImplementedError()


class Orchestrator:
    def __init__(self, broker, downloader_prx):
        self.orchestrators_dic = {}
        self.files_dic = {}
        self.adapter = broker.createObjectAdapter('OrchestratorAdapter')
        self.downloader = TrawlNet.DownloaderPrx.checkedCast(broker.stringToProxy(downloader_prx))

        if not self.downloader:
            raise ValueError(Color.BOLD + Color.RED + 'Invalid proxy ' + Color.END)

        # IceStorm connect with my_storm
        self.topic = my_storm.get_topic_manager(broker)
        if not self.topic:
            raise ValueError(Color.BOLD + Color.RED + 'Invalid proxy in topic manager' + Color.END)

        # Orchestrator subscriber event
        self.subscriber = OrchestratorEventI(self)
        self.subscriber_prx = self.adapter.addWithUUID(self.subscriber)  # proxy

        try:
            self.topic = self.topic.retrieve(my_storm.ORCHESTRATOR_TOPIC_NAME)
        except my_storm.EXCEPTION:
            self.topic = self.topic.create(my_storm.ORCHESTRATOR_TOPIC_NAME)

        self.topic.subscribeAndGetPublisher({}, self.subscriber_prx)

        # Orchestrator publisher event
        self.publisher = TrawlNet.OrchestratorEventPrx.uncheckedCast(self.topic.getPublisher())

        # Orchestrator servant
        self.servant = OrchestratorI(self, self.downloader)
        self.servant_prx = self.adapter.addWithUUID(self.servant)  # proxy

    def send_download_task(self, url):
        raise NotImplementedError()

    def new_orchestrator(self, orchestrator):
        raise NotImplementedError()

    def hello_to(self, orchestrator):
        raise NotImplementedError()

    def get_files(self):
        raise NotImplementedError()

    def start_servant(self):
        self.adapter.activate()

    def stop(self):
        self.topic.unsubscribe(self.subscriber_prx)


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


if __name__ == '__main__':
    sys.exit(Server().main(sys.argv))
