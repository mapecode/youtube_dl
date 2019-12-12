#!/usr/bin/python3
import sys
import Ice
from color import Color

""" si se recibe url se descargar si no se imprime la lista de ficheros"""
Ice.loadSlice('trawlnet.ice')
import TrawlNet


class Client(Ice.Application):
    def run(self, argv):
        broker = self.communicator()
        proxy = broker.stringToProxy(argv[1])
        orchestrator = TrawlNet.OrchestratorPrx.checkedCast(proxy)

        if not orchestrator:
            raise RuntimeError(Color.BOLD + Color.RED + 'Invalid proxy' + Color.END)
            print(Color.BOLD + Color.RED + 'Error en los argumentos \n'
                                           'Uso correcto: ./run_client <orchestrator_proxy> <file_url[optional]>' + Color.END)
        file_list = orchestrator.getFileList()
        if argv[2] == "" and len(file_list) is 0:
            print(Color.BOLD + Color.GREEN + "\n* Lista vacia... No hay ningun archivo descargado.\n" + Color.END)
        elif argv[2] == "":
            print(Color.BOLD + Color.GREEN + "\n* Files List: " + str(file_list).replace("[", "").replace("]", "") + "\n")
        else:
            print(Color.GREEN + "\n* mp3 downloaded: '" + Color.BOLD + str(
            orchestrator.downloadTask(argv[2])) + "'\n" + Color.END)

        return 0


if __name__ == '__main__':
    sys.exit(Client().main(sys.argv))
