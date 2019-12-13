#!/usr/bin/python3
# pylint: disable=C0114
import sys
import Ice
# pylint: disable=E0401
import color

Ice.loadSlice('trawlnet.ice')
# pylint: disable=C0413
import TrawlNet


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
            raise RuntimeError(color.BOLD + color.RED + 'Invalid proxy' + color.END)

        if args[2] == "":
            file_list = orchestrator.getFileList()
            if len(file_list) == 0:
                print(color.BOLD + color.YELLOW + "\n* The list is empty\n" + color.END)
            else:
                print(color.BOLD + color.GREEN + "Files List:" + color.END)
                for file_downloaded in file_list:
                    print(color.BOLD + color.GREEN + file_downloaded + color.END)
        else:
            try:
                file_downloaded = orchestrator.downloadTask(args[2])
                print(color.GREEN + color.BOLD + "\n" + str(file_downloaded) + "\n" + color.END)
            except TrawlNet.DownloadError as msg_exception:
                print(msg_exception)
            except ValueError as msg_exception:
                print(msg_exception)

        return 0


if __name__ == '__main__':
    sys.exit(Client().main(sys.argv))
