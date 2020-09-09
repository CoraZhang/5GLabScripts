'''
Created on 11 apr 2017

@author: emwtrxss
'''

from equipment.instrument.instrument import Instrument

class rohde_schwarz_nrp2(Instrument):
    
    def __init__(self, equipment_settings):
        '''
        Constructor
        '''
        super(rohde_schwarz_nrp2, self).__init__(equipment_settings)
    
    def preset(self):
        '''
        Init NRP
        '''
        scpi_cmd = '*RST;*CLS;*ESE 0; *SRE 0; STAT:PRESET'
        self.connection.send_command(scpi_cmd)
    
    def get_errors(self):
        '''
        Read errors
        '''
        resp = self.connection.send_query('SYSTem:ERRor:ALL?')
        return resp
        
    def set_center_freq(self, freq, unit = 'MHZ', sensor = 1):
        scpi_cmd = 'SENSe{}:FREQ {}{}'.format(sensor, freq, unit )
        self.connection.send_command(scpi_cmd)
        
    def get_center_freq(self, sensor = 1):
        scpi_cmd = "SENS{}:FREQ?".format(sensor)
        return self.connection.send_query(scpi_cmd)
    
    def set_reference_offset(self, value, sensor = 1):
        '''
        Update for NRP
        '''
        scpi_cmd = 'SENSe{}:CORR:OFFS {}DB'.format( sensor, value)
        self.connection.send_command(scpi_cmd)
        
    def get_reference_offset(self,sensor = 1):
        '''
        Update for NRP
        '''
        scpi_cmd = 'SENSe{}:CORR:OFFS?'.format(sensor)
        return self.connection.send_command(scpi_cmd)
    
    def set_offset_mode(self, mode, sensor = 1):
        '''
        update for NRP
        '''
        scpi_cmd = 'SENSe{}:CORR:OFFS:STAT {}'.format(sensor, mode)
        self.connection.send_command(scpi_cmd)
    
    def get_offset_mode(self, sensor = 1):
        '''
        Update for NRP
        '''
        scpi_cmd = 'SENSe{}:CORR:OFFS:STAT?'.format(sensor)
        return self.connection.send_command(scpi_cmd)
    
    def get_power_in_dbm(self, sensor = 1):
        """Measure power and return value in dBm"""
#        _nrp_time = time.time()

        scpi_cmd = 'INIT{}:CONT OFF'.format(sensor)
        self.connection.send_command(scpi_cmd)
        scpi_cmd = 'UNIT{}:POW DBM'.format(sensor)
        self.connection.send_command(scpi_cmd)
        scpi_cmd = 'INIT{}:IMM'.format(sensor)
        self.connection.send_command(scpi_cmd)
        scpi_cmd = 'FETCh{}?'.format(sensor)
        power = self.connection.send_query(scpi_cmd)
        scpi_cmd = 'INIT{}:CONT ON'.format(sensor)
        self.connection.send_command(scpi_cmd)
#            print time.time() - _nrp_time
        return power
    
if __name__ == '__main__':
    nrp_equipment_settings= {'id' : 'NRP1', 'connection':{'address':'TCPIP::150.132.17.164','type':'VISA','timeout':'20', 'delay':'0'}}
    nrp = rohde_schwarz_nrp2(nrp_equipment_settings)
    print nrp.IDN()