'''
Created on 14 apr 2017

@author: eerikni
'''

class Connection(object):
    '''
    classdocs
    '''


    def __init__(self, equipment_settings):
        '''
        Constructor
        '''
        self.equipment_settings = equipment_settings
        
    def send_command(self, command):
        '''
        Method must be overridden by sub-class.
        '''
        pass

    def send_query(self, command):
        '''
        Method must be overridden by sub-class.
        '''
        return None