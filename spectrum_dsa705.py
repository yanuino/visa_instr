from usbtmc_device import Usbtmc_Device
import time

class dsa705(Usbtmc_Device):
    def __init__(self):
        self.models = ['DSA705']
        self.idVendor = 0x1ab1
        self.idProduct = 0x0960

        super(dsa705, self).__init__(self.idVendor, self.idProduct)
    
    def portname(self):
        return 'usbtmc'

    def configure(self):
        self.instr.write('*RST')
        time.sleep(0.5)
        self.instr.write(':FREQ:START 150000')
        self.instr.write(':FREQ:STOP 30000000')
        self.instr.write(':POW:ATT 10')

        self.instr.write(':UNIT:POW DBUV')
        self.instr.write(':DISP:WIN:TRAC:Y:DLIN 68')
        self.instr.write(':DISP:WIN:TRAC:Y:DLIN:STAT ON')

        self.instr.write(':CALC:MARK:AOFF')
        self.instr.write(':CALC:MARK1:PEAK:SEAR:MOD MAX')
        self.instr.write(':CALC:MARK1:MOD POS')
        self.instr.write(':CALC:MARK2:PEAK:SEAR:MOD MAX')
        self.instr.write(':CALC:MARK2:MOD POS')
 
    def measure(self):
        self.instr.write(':CALC:MARK1:MAX:MAX')
        res_vmax = self.instr.ask('CALC:MARK1:Y?')
        vmax = float('{:.2f}'.format(float(res_vmax)))
        self.instr.write(':CALC:MARK2:MIN')
        res_vmin = self.instr.ask('CALC:MARK2:Y?')
        vmin = float('{:.2f}'.format(float(res_vmin)))
        return [ 'VMAX', vmax, 'dBuV', 'VMIN', vmin, 'dBuV']

    def meas_max(self):

        vmax = 0.0
        try:
            self.instr.write(':CALC:MARK1:MAX:MAX')
            res_vmax = self.instr.ask('CALC:MARK1:Y?')
            print(res_vmax)
            if res_vmax != "":
                vmax = float('{:.2f}'.format(float(res_vmax)))
        except:
            pass
        return vmax

    def local(self):
        ##TODO
        #self.instr.clear()
        self.instr.close()
        pass
