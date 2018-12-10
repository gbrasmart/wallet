#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pprint import pprint


from node import client



class mainController():
    m_client = None

    def __init__(self,public_key,private_key):
      self.m_client = client.NodeClient()
      self.m_client.set_keys(public_key,private_key)
      #TODO get data from somewhere
      self.m_client.connect("",0)

    def __del__(self):
        self.m_client.disconnect()

    def network_connected(self):
        return self.m_client.is_connected()

    def get_balance(self):
        return self.m_client.get_balance()

    def send_transaction(self,targetText,amountIntegral,amountFraction):
        return self.m_client.send_transaction()