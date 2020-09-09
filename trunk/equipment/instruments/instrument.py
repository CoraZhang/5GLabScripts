'''
Created on 10 Sep 2016

@author: eerikni
'''

from ..connection import stubbed
from ..connection import direct_serial
from ..connection import visa
from ..connection import socket_tcp
from ..connection import telnet


class Instrument(object):
    '''
    classdocs
    Base class for Insturments
        Should contain
        IP
        ID
        Type
        Communication
    '''
    
    def __init__(self, equipment_settings):
        self.connection_type = equipment_settings['connection']['type'].upper()
        self.equipment_settings = equipment_settings

        if self.connection_type =='VISA':
            self.connection = visa.Visa(equipment_settings)
        elif self.connection_type == 'SERIAL':
            self.connection = direct_serial.DirectSerial(equipment_settings)
        elif self.connection_type == 'STUBBED':
            self.connection = stubbed.Stubbed(equipment_settings)
        elif self.connection_type == 'SOCKET':
            self.connection = socket_tcp.SocketTCP(equipment_settings)
        elif self.connection_type == 'TELNET':  
            self.connection = telnet.Telnet(equipment_settings)

        import logging
        logging.debug('Connected to {} {}, {}' .format(equipment_settings['id'], 
                                                       equipment_settings['connection']['address'], 
                                                       self.IDN()))

    def preset(self):
        '''
        Must be overridden by subclass
        '''
        pass

    def IDN(self):
        if self.connection_type == 'VISA':
            scpi_cmd = '*IDN?'
            return self.connection.send_query(scpi_cmd)
        elif self.connection_type == 'SOCKET':
            scpi_cmd = '*IDN?'
            return self.connection.send_query(scpi_cmd)
        else: return None
#     def __init__(self, ip, ID, Type, communication = 'VISA'):
#         '''
#         Constructor
#         '''
#         self.IP = ip
#         self.ID = ID
#         self.Type = Type
#         self.Communication = communication.upper()
#         self._connect()
        
        
#     def _connect(self):
#         if self.Communication == 'VISA':
#             #import visa as vi
#             self.com = instrument('TCPIP::%s' %self.IP)
            
#     def send(self, cmd):
#         if self.Communication == 'VISA':
#             self.com.write(cmd)
#             print(cmd)
#     def query(self, cmd):
#         if self.Communication == 'VISA':
#             resp = self.com.ask(cmd)
#             print cmd, resp
#             return resp