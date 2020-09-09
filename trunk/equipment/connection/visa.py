'''
Created on 14 apr 2017

@author: eerikni
'''

import platform, logging

from connection import Connection

PLATFORM = platform.system()

'''
Try to import PyVisa module
It depends on that the visa Agilent/NI library exist on computer

.. todo:: This error handling must be improved.
'''
try:

#     if  PLATFORM == 'Windows':
#     from visa import *
#     rm = ResourceManager(r"C:\Windows\System32\visa32.dll")
    
    print 'YAS'
#     elif PLATFORM == 'Linux':
#         #visa_library.load_library(r"/usr/local/vxipnp/linux/bin/libvisa.so.7")
#         import pyvisa 
#         rm = pyvisa.ResourceManager('/usr/local/vxipnp/linux/bin/libvisa.so.7')
#     else:
#         print 'Does not match'

except Exception, error:
    logging.info("Could not load pyvisa: %s" % error)


class Visa(Connection):
    '''
    This class implements equipment communication through VISA.

    .. todo:: Error handling, check that the set values in the instrument
    '''

    def __init__(self, equipment_settings):
        super(Visa, self).__init__(equipment_settings)
        if equipment_settings:
            timeout_s = float(equipment_settings['connection']['timeout'])
            timeout_ms = timeout_s * 1000
            delay_s = float(equipment_settings['connection']['delay'])
            delay_ms = delay_s * 1000
            self.debug = equipment_settings['connection']['debug']
            try:
                if PLATFORM == 'Windows':
                    import pyvisa as vi
                    rm = vi.ResourceManager()
                    self.conn = rm.open_resource(equipment_settings['connection']['address'], timeout=timeout_s)
                elif PLATFORM == 'Linux':
                    self.conn = rm.open_resource(equipment_settings['connection']['address'])
                    self.conn.timeout = timeout_ms
            except:
                print("Failed to create VISA connection for equipment " + self.equipment_settings['id'] + ".")
                raise      
    
    def send_command(self, command):
        '''
        Sends SCPI command using specified VISA interface.
        '''
        if self.debug:
            print('Command sent to equipment ' +
                              self.equipment_settings['id'] + ' using VISA: ' +
                              command)
        self.conn.write(command)
    
    def send_query(self, command):
        '''
        Sends SCPI query using specified VISA interface, return list.
        '''
        self.send_command(command)
        ret_value = self.conn.read().split(',')
        if self.debug:
            print('Equipment ' + self.equipment_settings['id'] + ' responded ' + str(ret_value) + 'using VISA.')
        return ret_value