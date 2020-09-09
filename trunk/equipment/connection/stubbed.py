'''
Created on 17 apr 2017

@author: eerikni
'''

from connection import Connection

class Stubbed(Connection):
    '''
    Testclass
    '''
    def __init__(self, equipment_settings):
        '''
        Constructor
        '''
        super(Stubbed, self).__init__(equipment_settings)
        print '{} has connected.'.format(self.equipment_settings['id'])
        
    def send_command(self, command):
        if self.equipment_settings['connection']['debug']:
            print('Sent command: {}'.format(command))
        else:
            pass
        
    def send_query(self, command):
        if self.equipment_settings['connection']['debug']:
            print('Sent query {}'.format(command))
        else:
            pass