'''
Created on 19 jul 2017

@author: echhein
'''
from socket import AF_INET,SOCK_STREAM, socket
from connection import Connection
import logging

class SocketTCP(Connection):
    '''
    classdocs
    '''

    def __init__(self, equipment_settings):
        '''
        Constructor
        '''

        super(SocketTCP, self).__init__(equipment_settings)
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.settimeout(float(equipment_settings['connection']['timeout']))
        self.socket.connect((equipment_settings['connection']['address'], int(equipment_settings['connection']['port'])))
        self.id = equipment_settings['id']
        
    def send_command(self, command):
        emsg = bytes(command + '\r\n')
        logging.debug('{}: {}'.format(self.id, command))
        self.socket.send(emsg)

    def send_query(self, command):
        self.send_command(command)
        ret = ''
        while 1:
            res = self.socket.recv(2048)
            
            ret = ret + res

            if res.endswith('\n'):
                break
            elif res.endswith('\r\n'):
                break

#         print ret
        logging.debug('{}: {}'.format(self.id, ret.strip()))
        return ret.strip()

    def return_log(self):
        return self.logger

    def disconnect(self):
        self.socket.close()
