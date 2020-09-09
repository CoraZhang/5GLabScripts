'''
Created on 17 apr 2017

@author: eerikni
'''

from connection import Connection

import telnetlib
import re, time

class Telnet(Connection):


    def __init__(self, equipment_settings):
        
        address = equipment_settings['connection']['address']
        port = equipment_settings['connection']['port']
        timeout = int(equipment_settings['connection']['timeout'])
        
        
        self.conn  = telnetlib.Telnet(address, port)
        self.timeout = timeout 

    def close(self):
        self.conn.close()
        
    def send_command(self, command):
        self.conn.write(command + chr(13))
        
    def send_query(self, command):
        self.conn.write(command + chr(13))
        return self.conn.read_until('\r', self.timeout)
    
    def read_until(self, end_mark):
        return self.conn.read_until(end_mark)

if __name__ == '__main__':
    pass