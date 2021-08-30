from usbtmc_device import Usbtmc_Device
import time

class ds1052e(Usbtmc_Device):
    def __init__(self):

        self.models = ['DS1052e']
        self.idVendor = 0x1ab1
        self.idProduct = 0x0588

        super(ds1052e, self).__init__(self.idVendor, self.idProduct)
    
    def portname(self):
        return 'usbtmc'

    def configure(self):
        # configuring volt ripple measurement
        self.instr.write('*RST')
        self.instr.write(':CHAN2:DISP OFF')
        self.instr.write(':DISP:TYPE:VECT')
        self.instr.write(':CHAN1:OFFS -0.002')
        self.instr.write(':CHAN1:PROB 1')
        self.instr.write(':CHAN1:COUP AC')
        self.instr.write(':CHAN1:SCAL 0.010')
        self.instr.write(':TIM:SCAL 0.00002')
        self.instr.write(':ACQ:TYPE AVER')
        self.instr.write(':ACQ:AVER 128')
    
    def measure(self):
        time.sleep(1.0)
        res_vmax = self.instr.ask(':MEAS:VMAX? CHAN1')
        res_vmin = self.instr.ask(':MEAS:VMIN? CHAN1')
        vmax = float('{:.3f}'.format(float(res_vmax)))
        vmin = float('{:.3f}'.format(float(res_vmin)))
        return [ 'VMAX', vmax, 'V', 'VMIN', vmin, 'V']

    def meas_min(self):
        time.sleep(1.0)
        res_vmin = self.instr.ask(':MEAS:VMIN? CHAN1')
        vmin = float('{:.3f}'.format(float(res_vmin)))
        return vmin

    def meas_max(self):
        time.sleep(1.0)
        res_vmax = self.instr.ask(':MEAS:VMAX? CHAN1')
        vmax = float('{:.3f}'.format(float(res_vmax)))
        return vmax
        
    def local(self):
        ##TODO
        #self.instr.clear()
        self.instr.close()
        pass




