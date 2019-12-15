#!/usr/bin/python3
# pylint: disable=C0114
import sys
import os
import Ice
from download_mp3 import download_mp3_with_id
import my_storm

# pylint: disable=E0401, C0413
Ice.loadSlice('trawlnet.ice')
import TrawlNet


class DownloaderI(TrawlNet.Downloader):
    # pylint: disable=R0903
    """Downloader interface implementation for download files"""

    def __init__(self, publisher):
        """
        @param publisher: for update events channel
        """
        self.publisher = publisher

    # pylint: disable=C0103, W0613
    def addDownloadTask(self, url, current=None):
        """
        Download the video from url
        @param url: link to the video
        @param current:
        @return: file info
        """
        try:
            out_file, file_id = download_mp3_with_id(url)
        except Exception as msg_exception:
            raise TrawlNet.DownloadError(str(msg_exception))

        file = TrawlNet.FileInfo()
        file.name = os.path.basename(out_file)
        file.hash = file_id

        self.publisher.newFile(file)

        return file


class Server(Ice.Application):
    """
    Downloader Server
    """

    def run(self, args):
        """
        Run implementation
        @param args: execution arguments
        @return: success execution
        """
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
