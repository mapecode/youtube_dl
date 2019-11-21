#!/usr/bin/python3
import sys
import Ice
from color import Color

Ice.loadSlice('trawlnet.ice')
import TrawlNet


class Client(Ice.Application):
    def run(self, argv):
        broker = self.communicator()
        proxy = broker.stringToProxy(argv[1])
        orchestrator = TrawlNet.OrchestratorPrx.checkedCast(proxy)

        if not orchestrator:
            raise RuntimeError(Color.BOLD + Color.RED + 'Invalid proxy' + Color.END)

        print(Color.GREEN+"mp3 downloaded => '"+Color.BOLD+orchestrator.downloadTask(argv[2])+"'"+Color.END)

        return 0


if __name__ == '__main__':
    sys.exit(Client().main(sys.argv))
