#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=C0114, E0401


import os
import sys
import binascii

import Ice
import IceGrid

# pylint: disable=E0401, C0413
Ice.loadSlice('trawlnet.ice')
import TrawlNet


class TransferI(TrawlNet.Transfer):
    # pylint: disable=R0903
    """Transfer interface implementation for transfer files"""

    def __init__(self, file_path):
        """
        @param file_path: path of the file
        """
        self.file_ = open(file_path, 'rb')

    def recv(self, size, current):
        """
        For recieve date within transfer
        @param size:
        @param current:
        @return:
        """
        try:
            return str(binascii.b2a_base64(self.file_.read(size), newline=False))
        except Exception as msg_exception:
            raise TrawlNet.TransferError(str(msg_exception))

    def close(self, current):
        """
        For close the file descriptor
        @param current:
        """
        self.file_.close()

    def destroy(self, current):
        """
        For remove the transfer
        @param current:
        """
        try:
            current.adapter.remove(current.id)
            print('TRASFER DESTROYED', flush=True)
        except Exception as e:
            print(e, flush=True)


class TransferFactoryI(TrawlNet.TransferFactory):
    # pylint: disable=R0903
    """Transfer Factory interface implementation for create transfers"""

    def __init__(self, downloads_directory):
        """
        @param downloads_directory:
        """
        self.downloads_directory = downloads_directory

    def create(self, file_name, current):
        """
        For create a transfer
        @param file_name:
        @param current:
        @return: the transfer
        """
        file_path = os.path.join(self.downloads_directory, file_name)
        servant = TransferI(file_path)
        proxy = current.adapter.addWithUUID(servant)
        print('# New transfer for {} #'.format(file_path), flush=True)

        return TrawlNet.TransferPrx.checkedCast(proxy)


class Server(Ice.Application):
    """
    TransferFactory Server
    """

    def run(self, args):
        """
        Run implementation
        @return: success execution
        """
        broker = self.communicator()
        properties = broker.getProperties()

        servant = TransferFactoryI(properties.getProperty("DownloadsDirectory"))
        adapter = broker.createObjectAdapter('TransferAdapter')
        factory_id = properties.getProperty('Identity')
        proxy = adapter.add(servant, broker.stringToIdentity(factory_id))

        print('{}'.format(proxy), flush=True)

        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()

        return 0


if __name__ == '__main__':
    app = Server()
    exit_status = app.main(sys.argv)
    sys.exit(exit_status)
