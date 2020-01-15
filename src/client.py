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
        proxy = broker.stringToProxy(args[1])
        orchestrator = TrawlNet.OrchestratorPrx.checkedCast(proxy)

        if not orchestrator:
            raise RuntimeError(Color.BOLD + Color.RED + 'Invalid proxy' + Color.END)

        if args[2] == "":
            file_list = orchestrator.getFileList()
            if len(file_list) == 0:
                print(Color.BOLD + Color.YELLOW + "\n* The list is empty\n" + Color.END)
            else:
                print(Color.BOLD + Color.GREEN + "Files List:" + Color.END)
                for file_downloaded in file_list:
                    print(Color.BOLD + Color.GREEN + str(file_downloaded) + Color.END)
        else:
            try:
                file_downloaded = orchestrator.downloadTask(args[2])
                print(Color.GREEN + Color.BOLD + "\n" + str(file_downloaded) + "\n" + Color.END)
            except TrawlNet.DownloadError as msg_exception:
                print(msg_exception)
            except ValueError as msg_exception:
                print(msg_exception)

        return 0

    def transfer_request(self, file_name):
        remote_EOF = False
        BLOCK_SIZE = 1024

        try:
            transfer = self.orchestrator.getFile(file_name)
        except TrawlNet.TransferError as e:
            print(e.reason)
            return 1

        with open(os.path.join(DOWNLOADS_DIRECTORY, file_name), 'wb') as file_:
            global remote_EOF
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
        print('Transfer finished!')


if __name__ == '__main__':
    sys.exit(Client().main(sys.argv))
