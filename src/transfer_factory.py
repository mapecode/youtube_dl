#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import binascii

import Ice
import IceGrid

Ice.loadSlice('trawlnet.ice')
import TrawlNet


APP_DIRECTORY = './'
DOWNLOADS_DIRECTORY = os.path.join(APP_DIRECTORY, 'downloads')


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
    def create(self, file_name, current):
        file_path = os.path.join(DOWNLOADS_DIRECTORY, file_name)
        servant = TransferI(file_path)
        proxy = current.adapter.addWithUUID(servant)
        print('# New transfer for {} #'.format(file_path), flush=True)

        return TrawlNet.TransferPrx.checkedCast(proxy)


class Server(Ice.Application):
    def run(self, args):
        ic = self.communicator()
        properties = ic.getProperties()

        servant = TransferFactoryI()
        adapter = ic.createObjectAdapter('TransferAdapter')
        factory_id = properties.getProperty('TransferFactoryIdentity')
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


# Use this function to receive data in the client side.
# ------------------------------------------------------
# def transfer_request(self, file_name):
#     remote_EOF = False
#     BLOCK_SIZE = 1024
#     transfer = None

#     try:
#         transfer = self.orchestrator.getFile(file_name)
#     except TrawlNet.TransferError as e:
#         print(e.reason)
#         return 1

#     with open(os.path.join(DOWNLOADS_DIRECTORY, file_name), 'wb') as file_:
#         remote_EOF = False
#         while not remote_EOF:
#             data = transfer.recv(BLOCK_SIZE)
#             if len(data) > 1:
#                 data = data[1:]
#             data = binascii.a2b_base64(data)
#             remote_EOF = len(data) < BLOCK_SIZE
#             if data:
#                 file_.write(data)
#         transfer.close()

#     transfer.destroy()
#     print('Transfer finished!')