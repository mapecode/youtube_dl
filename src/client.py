#!/usr/bin/python3
# pylint: disable=C0114
import sys
import binascii
import os
import Ice
# pylint: disable=E0401
from utils import Color

Ice.loadSlice('trawlnet.ice')
# pylint: disable=C0413
import TrawlNet

APP_DIRECTORY = './'
DOWNLOADS_DIRECTORY = os.path.join(APP_DIRECTORY, 'downloads')


class Client(Ice.Application):
    """
    Client implementation for create the download requests
    """

    def run(self, args):
        """
        Run client implementation
        @param args: execution arguments
        @return: success execution
        """
        broker = self.communicator()

        if len(args) == 1:  # List request
            orchestrator = TrawlNet.OrchestratorPrx.checkedCast(
                broker.stringToProxy("OrchestratorServer1 -t -e 1.1 @ Orchestrator1.OrchestratorAdapter")
            )
            if not orchestrator:
                raise RuntimeError(Color.BOLD + Color.RED + 'Invalid proxy' + Color.END)

            file_list = orchestrator.getFileList()
            if len(file_list) == 0:
                print(Color.BOLD + Color.YELLOW + "\n* The list is empty\n" + Color.END)
            else:
                print(Color.BOLD + Color.GREEN + "Files List:" + Color.END)
                for file_downloaded in file_list:
                    print(Color.BOLD + Color.GREEN + str(file_downloaded) + Color.END)
        elif args[1] == '--download':  # Download request
            orchestrator = TrawlNet.OrchestratorPrx.checkedCast(
                broker.stringToProxy("OrchestratorServer2 -t -e 1.1 @ Orchestrator2.OrchestratorAdapter")
            )
            if not orchestrator:
                raise RuntimeError(Color.BOLD + Color.RED + 'Invalid proxy' + Color.END)
            try:
                url = input('Input the url \n> ')
                file_downloaded = orchestrator.downloadTask(url)
                print(Color.GREEN + Color.BOLD + "\n" + str(file_downloaded) + "\n" + Color.END)
            except TrawlNet.DownloadError as msg_exception:
                print(msg_exception)
            except ValueError as msg_exception:
                print(msg_exception)
        elif args[1] == '--transfer':  # Transfer request
            orchestrator = TrawlNet.OrchestratorPrx.checkedCast(
                broker.stringToProxy("OrchestratorServer3 -t -e 1.1 @ Orchestrator3.OrchestratorAdapter")
            )
            if not orchestrator:
                raise RuntimeError(Color.BOLD + Color.RED + 'Invalid proxy' + Color.END)
            try:
                file_name = input('Input the filename \n> ')
                self.transfer_request(orchestrator, file_name)
            except TrawlNet.TransferError as msg_exception:
                print(msg_exception)
        else:  # Invalid args
            print(Color.BOLD + Color.RED + "Arguments error" + Color.END)
            print(Color.BOLD + Color.GREEN + 'Examples:\n \
                * Download song: client.py --download <url> --Ice.Config=client.config\n \
                * Get List: client.py --Ice.Config=client.config\n \
                * Init transfer: client.py --transfer <file_name> --Ice.Config=client.config' + Color.END)

        return 0

    @staticmethod
    def transfer_request(orchestrator, file_name):
        BLOCK_SIZE = 1024

        try:
            transfer = orchestrator.getFile(file_name)
        except TrawlNet.TransferError as e:
            print(e.reason)
            return 1

        with open(os.path.join(DOWNLOADS_DIRECTORY, file_name), 'wb') as file_:
            remote_EOF = False

            while not remote_EOF:
                data = transfer.recv(BLOCK_SIZE)
                if len(data) > 1:
                    data = data[1:]
                data = binascii.a2b_base64(data)
                remote_EOF = len(data) < BLOCK_SIZE
                if data:
                    file_.write(data)
            transfer.close()

        transfer.destroy()
        print(Color.GREEN + Color.BOLD + 'Transfer finished!' + Color.END)


if __name__ == '__main__':
    sys.exit(Client().main(sys.argv))
