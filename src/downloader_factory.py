#!/usr/bin/python3
# pylint: disable=C0114, E0401
import sys
import os
import Ice
from utils import download_mp3_with_id, get_topic, get_topic_manager, DOWNLOADER_TOPIC_NAME

# pylint: disable=E0401, C0413
Ice.loadSlice('trawlnet.ice')
import TrawlNet


class DownloaderI(TrawlNet.Downloader):
    # pylint: disable=R0903
    """Downloader interface implementation for download files"""

    def __init__(self, publisher, downloads_directory):
        """
        @param publisher: for update events channel
        @param downloads_directory:
        """
        self.publisher = publisher
        self.downloads_directory = downloads_directory

    # pylint: disable=C0103, W0613
    def addDownloadTask(self, url, current=None):
        """
        Download the video from url
        @param url: link to the video
        @param current:
        @return: file info
        """
        try:
            out_file, file_id = download_mp3_with_id(url, destination=self.downloads_directory)
        except Exception as msg_exception:
            raise TrawlNet.DownloadError(str(msg_exception))

        file = TrawlNet.FileInfo()
        file.name = os.path.basename(out_file)
        file.hash = file_id

        self.publisher.newFile(file)

        return file

    def destroy(self, current):
        """
        For destroy a downloader
        @param current:
        """
        try:
            current.adapter.remove(current.id)
            print('TRANSFER DESTROYED', flush=True)
        except Exception as e:
            print(e)


class DownloaderFactoryI(TrawlNet.DownloaderFactory):
    # pylint: disable=R0903
    """Downloader Factory interface implementation for create downloaders"""

    def __init__(self, broker, downloads_directory):
        """
        @param broker: broker for operations
        @param downloads_directory: directory for downloads
        """
        self.broker = broker
        self.downloads_directory = downloads_directory

    def create(self, current=None):
        """
        For create a downloader
        @param current:
        @return: the downloader
        """
        topic_manager = get_topic_manager(self.broker)
        sync_topic = get_topic(topic_manager, DOWNLOADER_TOPIC_NAME)
        publisher = TrawlNet.UpdateEventPrx.uncheckedCast(sync_topic.getPublisher())

        servant = DownloaderI(publisher, self.downloads_directory)
        proxy = current.adapter.addWithUUID(servant)

        return TrawlNet.DownloaderPrx.checkedCast(proxy)


class Server(Ice.Application):
    """
    DownloaderFactory Server
    """

    def run(self, args):
        """
        Run implementation
        @return: success execution
        """
        broker = self.communicator()
        properties = broker.getProperties()
        adapter = broker.createObjectAdapter("DownloaderFactoryAdapter")

        servant = DownloaderFactoryI(broker, properties.getProperty("DownloadsDirectory"))
        factory_id = properties.getProperty('Identity')
        proxy = adapter.add(servant, broker.stringToIdentity(factory_id))

        print(proxy)
        sys.stdout.flush()

        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()

        return 0


if __name__ == '__main__':
    sys.exit(Server().main(sys.argv))
