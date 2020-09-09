'''
Created on 13 apr 2017

@author: eerikni
'''

from instrument import Instrument
from collections import OrderedDict
    
class rohde_schwarz_fsw(Instrument):
    '''
    classdocs
    '''
    
    def __init__(self, equipment_settings):
        '''
        Constructor
        '''
        super(rohde_schwarz_fsw, self).__init__(equipment_settings)

        
    def preset(self):
        '''
        Preset instrument
        '''
        scpi_cmd = "*RST;*CLS;*ESE 0; *SRE 0; STAT:PRESET"
        self.connection.send_command(scpi_cmd)
#         self.display_state_set('ON')
        
    def display_state_set(self, state='ON'):
        '''
        "SYSTem:DISPlay:UPDate ON|OFF
        '''
        scpi_cmd = "SYST:DISP:UPD {}".format(state)
        self.connection.send_command(scpi_cmd)
        
    def get_errors(self):
        '''
        Read errors
        '''
        resp = self.connection.send_query('SYSTem:ERRor?')
        return resp
    
    def continuous_state_set(self, state = 'ON'):
        scpi_cmd = 'INIT:CONT {}'.format(state)
        self.connection.send_command(scpi_cmd)
        
    def trigger_source_set(self, source = 'EXT'):
        ''' External = EXT
            IFPower = IFP
        '''
        scpi_cmd = 'TRIGger:SOURce {}'.format(source)
        self.connection.send_command(scpi_cmd)

    def trigger_level_set(self, level = '-45'):
        ''' 
        Set level of IFPower trigger 
        '''
        scpi_cmd = 'TRIGger:LEVel:IFPower {}dBm'.format(level)
        self.connection.send_command(scpi_cmd)

    def trigger_direction_set(self, trig = 2, direction = 'OUTPut'):
        '''
        set direction of trigger
        '''
        scpi_cmd = 'OUTPut:TRIGger{}:DIRection {}'.format(trig, direction)
        self.connection.send_command(scpi_cmd)

    def trigger_outputtype_set(self, trig = 2, variant = 'DEVice'):
        scpi_cmd = 'OUTPut:TRIGger{}:OTYPe {}'.format(trig, variant)
        self.connection.send_command(scpi_cmd)
    
    def trigger_sweep(self):
        scpi_cmd = 'INIT:IMM'
        self.connection.send_command(scpi_cmd)
#         return resp
    
    def trace_get(self, trace = 1):
        scpi_cmd = 'TRACe{}:DATA? TRACE1'.format(trace)
        resp = self.connection.send_query(scpi_cmd)
        return resp

    '''
    --------------- LTE OPTIONS ---------------
    '''
        
    def sel_opt_LTE(self, switch = 0):
        '''
        INSTrument[:SELect] LTE
        '''
        
        scpi_cmd = 'INST:SEL LTE'
        self.connection.send_command(scpi_cmd)
        
    def setup_EVM(self, FREQ = '1.94e9', ATT = '0', REFLVL = '-5', NRBRANCHES = '4', TESTMODEL = 'E-TM1_1__5MHz', BOOSTING = 3, CELLID = 1):
        self.sel_opt_LTE()
        self.connection.send_command('CONF:LTE:MEAS EVM')
        self.connection.send_command('INIT:CONT OFF')
        self.connection.send_command('FREQ:CENT {}'.format(FREQ))
        self.connection.send_query('INP:ATT {};*OPC?'.format(ATT))
        self.connection.send_query('DISP:TRAC:Y:RLEV {};*OPC?'.format(REFLVL))
        self.connection.send_query('MMEMory:LOAD:TMOD:DL \'{}\';*OPC?'.format(TESTMODEL))
        self.connection.send_query('CONFigure:LTE:DL:MIMO:CONFig TX{};*OPC?'.format(NRBRANCHES))
        self.connection.send_command('CONFigure:LTE:DL:REFSig:POWer {}'.format(BOOSTING))
        self.connection.send_command('CONFigure:LTE:DL:PLC:CID {}'.format(CELLID))
        
    def setup_EVM_SEL_BR(self, BRANCH = '1'):
        self.sel_opt_LTE()
        self.connection.send_query('CONFigure:LTE:DL:MIMO:ASELection ANT{};*OPC?'.format(BRANCH))    
    
    def setup_RS_RE_Meas(self, frequency, BW, nrbranches, branch = 1, cellID = 1, transmissionmode = '4', attenuation = '15', reflevel = '5'):
        '''
            Sets up measurement for returning Allocation Table, 
        '''        
        self.setup_EVM(FREQ = frequency, ATT = attenuation, REFLVL = reflevel, NRBRANCHES = nrbranches,TESTMODEL = 'E-TM1_1__{}MHz'.format(BW), BOOSTING = 0, CELLID = cellID)
        self.setup_EVM_SEL_BR('{}'.format(branch))
        self.connection.send_query('LAY:WIND2:REM;*OPC?')
        self.connection.send_query('LAY:WIND3:REM;*OPC?')
        self.connection.send_query('LAY:WIND4:REM;*OPC?')
        self.connection.send_query('LAY:WIND5:REM;*OPC?')
        self.connection.send_query('LAY:REPL:WIND \'1\',ASUM;*OPC?')
        self.connection.send_query('LAY:ADD? \'1\',ABOVe,CBUF;*OPC?')
        if transmissionmode == '9':
            self.connection.send_query('LAY:ADD? \'1\',BELow,IRWM;*OPC?')
            self.connection.send_query('CONFigure:LTE:DL:SUBFrame0:ALLoc0:PRECoding:SCH BF;*OPC?')
            self.connection.send_query('CONFigure:LTE:DL:SUBFrame0:ALLoc0:PRECoding:AP 7;*OPC?')
            self.connection.send_query('CONFigure:LTE:DL:CSIRs:STATe ON;*OPC?')
            self.connection.send_query('CONFigure:LTE:DL:CSIRs:CI 1;*OPC?')
            self.connection.send_query('CONfigure:LTE:DL:CSIRs:SCI 1;*OPC?')
            self.connection.send_query('CONFigure:LTE:DL:CSIRs:NAP TX8; *OPC?')
        self.get_errors() 
        
    def sel_opt_IQ(self):
        '''
        INSTrument[:SELect] IQ
        '''
        
        scpi_cmd = 'INST:SEL IQ'
        self.connection.send_command(scpi_cmd)
    
    def take_CSI_Meas(self):

        ret_csi = OrderedDict()

        csi1 = self.connection.send_query('TRACe3:DATA? TRACE1')
        self.get_errors()
        ret_csi['csi1'] = csi1
        csi2 = self.connection.send_query('TRACe3:DATA? TRACE2')
        self.get_errors()
        ret_csi['csi2'] = csi2
        csi3 = self.connection.send_query('TRACe3:DATA? TRACE3')
        self.get_errors()
        ret_csi['csi3'] = csi3
        csi4 = self.connection.send_query('TRACe3:DATA? TRACE4')
        self.get_errors()
        ret_csi['csi4'] = csi4
        csi5 = self.connection.send_query('TRACe3:DATA? TRACE5')
        self.get_errors()
        ret_csi['csi5'] = csi5
        csi6 = self.connection.send_query('TRACe3:DATA? TRACE6')
        self.get_errors()
        ret_csi['csi6'] = csi6
        csi7 = self.connection.send_query('TRACe3:DATA? TRACE7')
        self.get_errors()
        ret_csi['csi7'] = csi7
        csi8 = self.connection.send_query('TRACe3:DATA? TRACE8')
        self.get_errors()
        ret_csi['csi8'] = csi8

        return ret_csi

    def trigger_EVM_Sweep(self):
        self.connection.send_query('INST:SEL LTE;*OPC?')
        self.connection.send_command('INIT:CONT OFF')
        self.connection.send_query('INIT:IMM;*OPC?')
        self.get_errors()

    def take_allocation_Meas(self):
        ret_alloc = OrderedDict()
        #self.connection.send_query('INST:SEL LTE;*OPC?')
        self.get_errors()
        self.connection.send_command('*WAI')
        allocation = self.connection.send_query('TRACe1:DATA? TRACE1')
        self.get_errors()
        ret_alloc['allocation'] = allocation
        
        return ret_alloc

    def setup_ACLR_Meas(self, frequency, BW, att = 15):
        OBW = str(float(BW)*0.9)

        self.connection.send_command('INST:SEL SAN')
        self.connection.send_command('CALC:MARK:FUNC:POWer:PRESet EUTRa')
        self.connection.send_command('INIT:CONT OFF')
        self.connection.send_command('FREQ:CENT {}'.format(frequency))
        self.connection.send_query('INP:ATT {};*OPC?'.format(att))
        '''Set to real OBW of 15MHz carrier'''
        self.connection.send_command('SENSe:POW:ACH:BAND:CHAN {}MHz'.format(OBW))
        self.connection.send_command('SENSe:POW:ACH:BAND:ACH {}MHz'.format(OBW))
        self.connection.send_command('SENSe:POW:ACH:SPACing:CHAN {}MHz'.format(BW))
        self.connection.send_command('SENSe:POW:ACH:SPACing:ACH {}MHz'.format(BW))
        
    def trigger_ACLR_Sweep(self):
        self.connection.send_query('INST:SEL SAN;*OPC?')
        self.connection.send_query('INIT:IMM;*OPC?')
    
    def take_ACLR_Meas(self):
        self.connection.send_query('INST:SEL SAN;*OPC?')
        resp = self.connection.send_query('CALCulate:MARKer:FUNCtion:POWer:RESult? ACPower')
        return resp
    
if __name__ == '__main__':
    fsw_equipment_settings= {'id' : 'SPEC1', 
                             'connection':{'address':'TCPIP::150.132.17.2',
                                           'type':'VISA',
                                           'timeout':'20', 
                                           'delay':'0'}}
    
    print fsw_equipment_settings['connection']
    
    spec = rohde_schwarz_fsw(fsw_equipment_settings)
    
    print spec.IDN()
