'''
Created on 17 apr 2017

@author: eerikni
'''

from connection import Connection
import time

try:
    import serial

except Exception, error:
    print ("Could not load pySerial: %s" % error)

class DirectSerial(Connection):
    '''
    Direct Serial communication
    '''


    def __init__(self, equipment_settings):
        '''
        Constructor
        '''
        super(DirectSerial, self).__init__(equipment_settings)
#         try:
        self.conn = serial.Serial()
        self.conn.bytesize = int(equipment_settings['connection']['bytesize'])
        self.conn.baudrate = int(equipment_settings['connection']['baudrate'])
        self.conn.stopbits = float(equipment_settings['connection']['stop_bits'])
        self.conn.parity = (equipment_settings['connection']['parity'][:1]).upper()
        self.conn.timeout = None
        self.conn.port = equipment_settings['connection']['address']
        self.conn.open()
#         self.supervisor.info("Serial configuration parameter 'flow control' is not implemented.")
        # If equipment is reset during port open, wait some time to let start up messages
        # be written out before flushing buffers.
        time.sleep(1)
        self.conn.flushInput()
        self.conn.flushOutput()
#         except:
#             print("Unable to create serial connection at " + equipment_settings['connection']['device'] + 
#                                   " for equipment id " + equipment_settings['id'] + " (" + 
#                                   equipment_settings['type'] + ").")
    
    def send_command(self, command):
        #print('Command sent to equipment ' +
#                               self.equipment_settings['id'] + ' using SERIAL: ' +
#                               command)
        # Get rid of anything sent by the terminal equipment as a response to any previous command
        self.conn.flushInput()
        
        self.conn.write(command + chr(10) + chr(13))
        time.sleep(0.5)
    
    def send_query(self, command):
        self.conn.flush()
        ch = u''
        terminal_response = u''
        self.conn.write(command + chr(13))
        # Currently, local echo at terminal equipment is assumed by this driver,
        # get rid of the local echo, last character is assumed to be Carriage Return
        while ch != chr(13):
            ch = self.conn.read(1)
        ch = u''
        # Read response until EOL (EOL assumed to be Carriage Return for reception)
        while ch != chr(13):
            # Store character as a part of the result if not a new line character
            if ch != chr(10):
                terminal_response = terminal_response + ch
            ch = self.conn.read(1)
        # Only first row is taken into account, get rid of others
        #print('Equipment ' + self.equipment_settings['id'] + ' responded ' + str(terminal_response) + 'using VISA.')
        return terminal_response
    
    def read_line(self):
        return self.conn.readline()
    
    def close(self):
        self.conn.close()
