#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import binascii

import Ice
import IceGrid

Ice.loadSlice('trawlnet.ice')
import TrawlNet


class TransferI(TrawlNet.Transfer):
    def __init__(self, file_path):
        self.file_ = open(file_path, 'rb')

    def recv(self, size, current):
        return str(binascii.b2a_base64(self.file_.read(size), newline=False))

    def close(self, current):
        self.file_.close()

    def destroy(self, current):
        try:
            current.adapter.remove(current.id)
            print('TRASFER DESTROYED', flush=True)
        except Exception as e:
            print(e, flush=True)


class TransferFactoryI(TrawlNet.TransferFactory):
    def __init__(self, downloads_directory):
        self.downloads_directory = downloads_directory

    def create(self, file_name, current):
        file_path = os.path.join(self.downloads_directory, file_name)
        servant = TransferI(file_path)
        proxy = current.adapter.addWithUUID(servant)
        print('# New transfer for {} #'.format(file_path), flush=True)

        return TrawlNet.TransferPrx.checkedCast(proxy)


class Server(Ice.Application):
    def run(self, args):
        ic = self.communicator()
        properties = ic.getProperties()

        servant = TransferFactoryI(properties.getProperty("DownloadsDirectory"))
        adapter = ic.createObjectAdapter('TransferAdapter')
        factory_id = properties.getProperty('Identity')
        proxy = adapter.add(servant, ic.stringToIdentity(factory_id))

        print('{}'.format(proxy), flush=True)

        adapter.activate()
        self.shutdownOnInterrupt()
        ic.waitForShutdown()

        return 0


if __name__ == '__main__':
    app = Server()
    exit_status = app.main(sys.argv)
    sys.exit(exit_status)
