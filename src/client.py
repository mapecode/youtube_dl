#!/usr/bin/python3
import sys
import Ice
import color
Ice.loadSlice('trawlnet.ice')
import TrawlNet


class Client(Ice.Application):
    def run(self, argv):
        broker = self.communicator()
        proxy = broker.stringToProxy(argv[1])
        orchestrator = TrawlNet.OrchestratorPrx.checkedCast(proxy)

        if not orchestrator:
            raise RuntimeError(color.BOLD + color.RED + 'Invalid proxy' + color.END)

        file_list = orchestrator.getFileList()
        if argv[2] == "" and len(file_list) is 0:
            print(color.BOLD + color.YELLOW + "\n* The list is empty\n" + color.END)
        elif argv[2] == "":
            print(color.BOLD + color.GREEN + "Files List:" + color.END)
            for file_downloaded in file_list:
                print(color.BOLD + color.GREEN + str(file_downloaded) + color.END)
        else:
            try:
                file_downloaded = orchestrator.downloadTask(argv[2])
                print(color.GREEN + "\n* mp3 downloaded: '" + color.BOLD + str(file_downloaded) + "'\n" +
                      color.END)
            except TrawlNet.DownloadError as e:
                print(e)

        return 0


if __name__ == '__main__':
    sys.exit(Client().main(sys.argv))
