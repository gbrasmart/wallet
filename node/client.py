#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pprint import pprint
import binascii
import socket
import logging
import random

from node import proto

buffer_size = 32


class Amount(object):
    def __init__(self):
        self.integral = 0
        self.fraction = 0

    def set_amount(self, integral=None, fraction=None):
        if integral is not None:
            self.integral = integral
        if fraction is not None:
            self.fraction = fraction


class Counters(object):
    def __init__(self):
        self.blocks = 0
        self.transactions = 0

    def set_vals(self, blocks=None, transactions=None):
        if blocks is not None:
            self.blocks = blocks
        if transactions is not None:
            self.transactions = transactions


class Transaction(object):
    def __init__(self):
        self.hash_hex = None
        self.sender_public = None
        self.receiver_public = None
        self.amount = Amount()
        self.currency = None

        self.salt = None

    def parse(self, proto_transaction_values):
        self.hash_hex = binascii.hexlify(proto_transaction_values[0])
        self.sender_public = binascii.hexlify(proto_transaction_values[1])
        self.receiver_public = binascii.hexlify(proto_transaction_values[2])
        self.amount.set_amount(
            integral=proto_transaction_values[3],
            fraction=proto_transaction_values[4]
        )
        self.currency = proto_transaction_values[5].decode("utf-8").rstrip('\0')


class Block(object):
    def __init__(self):
        self.hash = None
        self.hash_hex = None

    def set_hash(self, data):
        if isinstance(data, bytes):
            self.hash = data
            self.hash_hex = binascii.hexlify(data)


class NodeClient(object):
    host = '127.0.0.1'
    port = 38100
    connected = False
    sock_timeout = 1000
    request = None
    response = None

    private_key = None
    public_key = None

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if self.sock_timeout is not None:
            self.sock.settimeout(self.sock_timeout)

    def set_keys(self,pub_key,pr_key):
        self.private_key = pr_key
        self.public_key = pub_key

    def connect(self, host=None, port=None):
        if host is not None:
            self.host = host
        if port is not None:
            self.port = port
        server_address = (self.host, self.port)
        try:
            self.sock.connect(server_address)
            self.connected = True
        except Exception as e:
            logging.error(str(e))

    def disconnect(self):
        if self.connected:
            self.sock.close()

    def is_connected(self):
        if self.connected:
            return True
        logging.error("no connection")
        return False

    def get_balance(self):
        if not self.is_connected():
            return
        self.request = proto.GetBalance()
        self.sock.sendall(self.request.buffer.raw)
        req_term = proto.TerminatingBlock()
        req_term.pack()
        self.sock.sendall(req_term.buffer.raw)

        self.response = proto.Header()
        self.sock.recv_into(self.response.buffer, self.response.structure.size)
        self.response.unpack()
        if not self.response.check_cmd_num('SendBalance'):
            return

        balance = proto.Balance()
        self.sock.recv_into(balance.buffer, balance.structure.size)
        balance.unpack()

        resp_term = proto.TerminatingBlock()
        self.sock.recv_into(resp_term.buffer, resp_term.structure.size)
        resp_term.unpack()

        amount = Amount()
        amount.set_amount(balance.integral, balance.fraction)
        return amount

    def get_counters(self):
        if not self.connected:
            logging.error("no connection")
            return

        self.request = proto.GetCounters()
        self.sock.sendall(self.request.buffer.raw)
        req_term = proto.TerminatingBlock()
        req_term.pack()
        self.sock.sendall(req_term.buffer.raw)

        self.response = proto.Header()
        self.sock.recv_into(self.response.buffer, self.response.structure.size)
        self.response.unpack()
        if not self.response.check_cmd_num('SendCounters'):
            return

        r_counters = proto.Counters()
        self.sock.recv_into(r_counters.buffer, r_counters.structure.size)
        r_counters.unpack()

        resp_term = proto.TerminatingBlock()
        self.sock.recv_into(resp_term.buffer, resp_term.structure.size)
        resp_term.unpack()

        counters = Counters()
        counters.set_vals(r_counters.blocks, r_counters.transactions)
        return counters

    def get_last_hash(self):
        if not self.is_connected():
            return

        self.request = proto.GetLastHash()
        self.sock.sendall(self.request.buffer.raw)
        req_term = proto.TerminatingBlock()
        req_term.pack()
        self.sock.sendall(req_term.buffer.raw)

        self.response = proto.Header()
        self.sock.recv_into(self.response.buffer, self.response.structure.size)
        self.response.unpack()
        if not self.response.check_cmd_num('SendLastHash'):
            return

        r_block_hash = proto.BlockHash()
        self.sock.recv_into(r_block_hash.buffer, r_block_hash.structure.size)
        r_block_hash.unpack()

        resp_term = proto.TerminatingBlock()
        self.sock.recv_into(resp_term.buffer, resp_term.structure.size)
        resp_term.unpack()

        block = Block()
        block.set_hash(r_block_hash.get_hash())
        return block

    def get_block_size(self, block_hash):
        if not self.is_connected():
            return
        self.request = proto.GetBlockSize(block_hash)
        self.sock.sendall(self.request.buffer.raw)
        req_term = proto.TerminatingBlock()
        req_term.pack()
        self.sock.sendall(req_term.buffer.raw)

        self.response = proto.Header()
        self.sock.recv_into(self.response.buffer, self.response.structure.size)
        self.response.unpack()
        if not self.response.check_cmd_num('SendBlockSize'):
            return

        r_block_hash = proto.BlockHash()
        self.sock.recv_into(r_block_hash.buffer, r_block_hash.structure.size)
        r_block_hash.unpack()

        block_size = proto.BlockSize()
        self.sock.recv_into(block_size.buffer, block_size.structure.size)
        block_size.unpack()

        resp_term = proto.TerminatingBlock()
        self.sock.recv_into(resp_term.buffer, resp_term.structure.size)
        resp_term.unpack()

        block_size = block_size.values[0]
        return block_size

    def get_transactions(self, block_hash, offset, limit):
        if not self.is_connected():
            return
        self.request = proto.GetTransactions(block_hash, offset, limit)
        self.sock.sendall(self.request.buffer.raw)
        req_term = proto.TerminatingBlock()
        req_term.pack()
        self.sock.sendall(req_term.buffer.raw)

        self.response = proto.Header()
        self.sock.recv_into(self.response.buffer, self.response.structure.size)
        self.response.unpack()

        txs = []
        if not self.response.check_cmd_num('SendTransactions'):
            return txs
        if not self.response.check():
            return txs

        tx_size = proto.calcsize('=%s' % proto.F_TRANSACTION)
        block_size = proto.calcsize('=%s' % proto.F_HASH)
        txs_size = self.response.size - block_size

        r_block_hash = proto.BlockHash()
        self.sock.recv_into(r_block_hash.buffer, r_block_hash.structure.size)
        r_block_hash.unpack()

        if txs_size % tx_size > 0:
            return txs
        txs_count = int(txs_size / tx_size)
        for i in range(0, txs_count):
            tx = proto.Transaction()
            self.sock.recv_into(tx.buffer, tx.structure.size)
            tx.unpack()
            # pprint(tx.values)
            t = Transaction()
            t.parse(tx.values)
            txs.append(t)
        return txs

    def get_blocks(self, offset, limit):
        if not self.connected:
            logging.error("no connection")
            return
        self.request = proto.GetBlocks(offset, limit)
        self.sock.sendall(self.request.buffer.raw)
        req_term = proto.TerminatingBlock()
        req_term.pack()
        self.sock.sendall(req_term.buffer.raw)

        self.response = proto.Header()
        self.sock.recv_into(self.response.buffer, self.response.structure.size)
        self.response.unpack()
        if not self.response.check_cmd_num('SendBlocks'):
            return

        blocks = []
        if self.response.size == 0:
            return blocks
        block_size = proto.calcsize(proto.F_HASH)
        if self.response.size % block_size > 0:
            return blocks
        blocks_count = int(self.response.size / block_size)
        for b in range(0, blocks_count):
            block_hash = proto.BlockHash()
            self.sock.recv_into(block_hash.buffer, block_hash.structure.size)
            block_hash.unpack()
            block = Block()
            block.set_hash(block_hash.get_hash())
            blocks.append(block)
        return blocks

    def get_transaction(self, b_hash, t_hash):
        if not self.is_connected():
            return
        self.request = proto.GetTransaction(b_hash, t_hash)
        self.sock.sendall(self.request.buffer.raw)
        req_term = proto.TerminatingBlock()
        req_term.pack()
        self.sock.sendall(req_term.buffer.raw)

        self.response = proto.Header()
        self.sock.recv_into(self.response.buffer, self.response.structure.size)
        self.response.unpack()
        if not self.response.check_cmd_num('SendTransaction'):
            return

        block_hash = proto.BlockHash()
        self.sock.recv_into(block_hash.buffer, block_hash.structure.size)
        block_hash.unpack()

        signature = proto.Signature()
        self.sock.recv_into(signature.buffer, signature.structure.size)
        signature.unpack()

        pub_key = proto.PublicKey()
        self.sock.recv_into(pub_key.buffer, pub_key.structure.size)
        pub_key.unpack()

        tx_data = proto.TransactionData()
        self.sock.recv_into(tx_data.buffer, tx_data.structure.size)
        tx_data.unpack()

        pprint(tx_data.buffer.raw)
        pprint(pub_key.buffer.raw)
        pprint(signature.buffer.raw)

        from racrypt import RaCryptLib
        import racrypt
        from os import path

        lib = racrypt.RaCryptLib()
        pprint(path.dirname(racrypt.__file__))
        lib.load(path.dirname(racrypt.__file__))
        res = lib.verify(
            data=tx_data.buffer.raw,
            pub_key=pub_key.buffer.raw,
            signature=signature.buffer.raw
        )
        pprint(res)



        # transaction = proto.Transaction()
        # self.sock.recv_into(transaction.buffer, transaction.structure.size)
        # transaction.unpack()
        # pprint(transaction.values)

        resp_term = proto.TerminatingBlock()
        self.sock.recv_into(resp_term.buffer, resp_term.structure.size)
        resp_term.unpack()

        t = Transaction()
        # t.parse(transaction.values)
        return t

    #TODO get from UI preTransaction without signature
    def send_transaction(self,target,
                            amountIntegral,amountFraction):
        if not self.is_connected():
            logging.error("no connection")
            return False

        #TODO sign Transaction

        import racrypt
        from os import path

        lib = racrypt.RaCryptLib()
        pprint(path.dirname(racrypt.__file__))
        lib.load(path.dirname(racrypt.__file__))



        t = Transaction()
        t.hash_hex = (b'c1c02d12cdadbc73da73cbd9985b2a41ffdb8dba9de470eaab453cc3595'
                  b'eab31f84bbe0766aea98b7ab5487eb5f962fc9c3ed6b6119600428d55ba'
                  b'd383be5020')
        t.sender_public = self.public_key
        t.receiver_public = target
        t.amount.integral = amountIntegral
        t.amount.fraction = amountFraction
        t.currency = b'RAS'
        t.salt = bytearray(buffer_size)
        for it in range(buffer_size):
            target[it] = random.randint(0, 255)

        lib.sign(0,188
          ,self.public_key,
          self.private_key
        )

        #send
        self.request = proto.SendTransaction(t)
        self.sock.sendall(self.request.buffer.raw)
        req_term = proto.TerminatingBlock()
        req_term.pack()
        self.sock.sendall(req_term.buffer.raw)

        #receive
        self.response = proto.Header()
        self.sock.recv_into(self.response.buffer, self.response.structure.size)
        self.response.unpack()
        if not self.response.check_cmd_num('Error'):
            logging.error("Node didnt getTransaction")
            return False

        resp_term = proto.TerminatingBlock()
        self.sock.recv_into(resp_term.buffer, resp_term.structure.size)
        resp_term.unpack()

        return True



if __name__ == '__main__':
    pass
