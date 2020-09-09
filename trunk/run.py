'''
Created on 11 dec. 2018

@author: eerikni
'''
from equipment.connection.direct_serial import DirectSerial
from equipment.instruments.rohde_schwarz_fsw import rohde_schwarz_fsw
import logging, time

class Table():
    def __init__(self, equipment_settings):
        self.conn = DirectSerial(equipment_settings)
    
    def move_to_position(self, position):
        cmd = 'pp{}'.format(position)
        self.conn.send_command(cmd)
        
        self.conn.read_line()
    
    def check_position(self):
        self.conn.send_command('pp')
        self.conn.read_line()
        return self.conn.read_line().strip()
    def set_speed(self, speed):
        cmd = 'ps{}'.format(speed)
        self.conn.send_command(cmd)
        
        self.conn.read_line()

if __name__ == '__main__':
    print('does this work?')
    
    spec_equipment_settings     = {'id' : 'SPEC_1',
                               'connection':{'address':'GPIB0::19::INSTR',
                                             'type':'VISA',
                                             'port': '5025',
                                             'timeout':'60',
                                             'delay':'0',
                                             'debug':'False'}}
    
#     spec = rohde_schwarz_fsw(spec_equipment_settings)
#     spec.IDN

    table_equipment_settings     = {'id' : 'Table_1',
                           'connection':{'address':'com4',
                                         'type':'SERIAL',
                                         'timeout':'20',
                                         'bytesize':'8',
                                         'baudrate':'115200',
                                         'stop_bits':'1',
                                         'parity':'n',
                                         'debug':'False'}}
    
    spec = rohde_schwarz_fsw(spec_equipment_settings)
#     spec.IDN()
#     import visa as vi
#     rm = vi.ResourceManager()
#     inst = rm.open_resource('GPIB0::19::INSTR')
 
    turnTable = Table(table_equipment_settings)
    turnTable.set_speed(1500)
    turnTable.move_to_position(3000)
    time.sleep(6)
    turnTable.set_speed(300)
    time.sleep(.2)
     
    turnTable.move_to_position(-3000)
    time.sleep(.1)
    spec.trigger_sweep()
#     
    import re,csv
#     
#     print turnTable.check_position()
     
    time.sleep(40)
    
    trace = spec.trace_get()
    new_trace = []
    for a in trace:
        new_trace.append(float(a.strip()))
    
    with open('test_wb63_1.csv', 'wb') as f:
        writer = csv.writer(f)
        writer.writerow(new_trace)
    
#     time.sleep(20)
#     turnTable.check_position()

#     import serial
#     c = serial.Serial()
#     c.baudrate = 115200
#     c.port = 'com4'
#     c.open()
#     
#     c.write('pp\r\n')
#     print c.readline()
#     print c.readline()
#     c.write('ps1500\r\n')
#     print c.readline()
#     print c.readline()
#     c.write('pp3000\r\n')
#     print c.readline()
#     print c.readline()
#     turnTable.move_to_position(-3000)
#     
#     print(turnTable.check_position())