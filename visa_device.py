""" If you cannot access your device without running your script as root,
then you may need to create a udev rule to properly set the permissions of the device.
First, connect your device and run lsusb. Find the vendor and product IDs.
Then, create a file /etc/udev/rules.d/visa.rules with the following content:

# VISA instruments
# Rigol DSA705
SUBSYSTEMS=="usb", ACTION=="add", ATTRS{idVendor}=="1ab1", ATTRS{idProduct}=="0960", GROUP="usbtmc", MODE="0660
# Rigol DS1052e
SUBSYSTEMS=="usb", ACTION=="add", ATTRS{idVendor}=="1ab1", ATTRS{idProduct}=="0588", GROUP="usbtmc", MODE="0660

You will also need to create the visa group and add yourself to it or substitute another group of your choosing """

import pyvisa

class PyVISA_Device(object):
    def __init__(self, scope_id = None, spectrum_id = None, multimeter_id = None):
        self.scope = None
        self.spectrum = None
        self.multimeter  = None
        
        self.rm = pyvisa.ResourceManager('@py')
        print('--VISA RM Session: {}'.format(self.rm.session))
        
        if scope_id is not None:
            print('--VISA Scope: tryingi {}'.format(scope_id))
            visa_scope_id = self.rm.list_resources(query = 'USB[0-9]*::' + scope_id + '?*::INSTR')
            if len(visa_scope_id) > 0:
                print('--VISA Scope: found "{}"'.format(visa_scope_id))
                try:
                    self.scope = self.rm.open_resource(visa_scope_id[0])
                    print('--VISA Scope: success')
                except:
                    print('--VISA Scope: error')
            else:
                print('--VISA Scope: "{}" not found'.format(scope_id))

        if spectrum_id is not None:
            print('--VISA Spectrum: trying {}'.format(spectrum_id))
            visa_spectrum_id = self.rm.list_resources(query = 'USB[0-9]*::' + spectrum_id + '?*::INSTR')
            if len(visa_spectrum_id) > 0:
                print('--VISA Scope: found "{}"'.format(visa_spectrum_id))
                try:
                    self.spectrum = self.rm.open_resource(visa_spectrum_id[0])
                    print('--VISA Scope: success')
                except:
                    print('--VISA Scope: error')
            else:
                print('--VISA Scope: "{}"" not found'.format(spectrum_id))
                          
        if multimeter_id is not None:
            print('--VISA Multimeter: trying {}'.format(multimeter_id))
            visa_multimeter_id = self.rm.list_resources(query = 'ASRL' + multimeter_id + '?*::INSTR')
            if len(visa_multimeter_id) > 0:
                print('--VISA Scope: found "{}"'.format(visa_multimeter_id))
                try:
                    self.multimeter = self.rm.open_resource(visa_multimeter_id[0], baud_rate = 4800, flow_control = pyvisa.constants.VI_ASRL_FLOW_XON_XOFF)
                    print('--VISA Scope: success')
                except:
                    print('--VISA Scope: error')
            else:
                print('--VISA Scope: "{}"" not found'.format(visa_multimeter_id))

    @property
    def resources(self):
        return self.rm.list_resources('?*::INSTR')

    def close(self):
        self.rm.close()

    @property
    def scope_detected(self):
        if self.scope is not None:       
            return True
        return False

    @property
    def scope_ident(self):
        if self.scope_detected:
            return self.scope.query('*IDN?')

    def scope_config_riple(self):
        if self.scope_detected:
            # configuring volt ripple measurement
            self.scope.write('*RST')
            self.scope.write(':CHAN2:DISP OFF')
            self.scope.write(':DISP:TYPE:VECT')
            self.scope.write(':CHAN1:OFFS -0.002')
            self.scope.write(':CHAN1:PROB 1')
            self.scope.write(':CHAN1:COUP AC')
            self.scope.write(':CHAN1:SCAL 0.020')
            self.scope.write(':TIM:SCAL 0.00002')
            self.scope.write(':ACQ:TYPE AVER')
            self.scope.write(':ACQ:AVER 128')
            return 'DONE'
        return 'ERR'

    def scope_meas_vmin(self):
        if self.scope_detected:
            res_vmin = self.scope.query(':MEAS:VMIN? CHAN1')
            vmin = '{:.3f}'.format(float(res_vmin))
            return vmin
        return 'ERR'

    def scope_meas_vmax(self):
        if self.scope_detected:
            res_vmax = self.scope.query(':MEAS:VMAX? CHAN1')
            vmax = '{:.3f}'.format(float(res_vmax))
            return vmax
        return 'ERR'

    def scope_close(self):
        self.scope.close()

    @property
    def multimeter_detected(self):
        if self.multimeter is not None:       
            return True
        return False

    @property
    def multimeter_ident(self):
        if self.multimeter_detected:
            return self.multimeter.query('*IDN?')

    def multimeter_config_dc(self):
        if self.multimeter_detected:
            # configuring volt dc measurement
            self.multimeter.write('*CLS')
            self.multimeter.write('FUNC \"VOLT\"')
            ### if most problems, insert error management (SYST:ERR? => Noerror | SettinConflict ...)
            self.multimeter.write('INP:COUP DC')
            self.multimeter.write('RANG:AUTO 0')
            self.multimeter.write('RANG 10.0')
            self.multimeter.write('FILT 0')
            return 'DONE'
        return 'ERR'
    
    def multimeter_measure(self):
        if self.multimeter_detected:
            res = self.multimeter.query('READ?')
            val = res.split()
            res =val[0]
            return res
        return 'ERR'

    @property
    def spectrum_detected(self):
        if self.spectrum is not None:       
            return True
        return False

    @property
    def spectrum_ident(self):
        if self.spectrum_detected:
            return self.spectrum.query('*IDN?')
    
    def spectrum_config(self):
        if self.spectrum_detected:
            self.spectrum.write('*RST')
            #time.sleep(0.5)
            self.spectrum.write(':FREQ:START 150000')
            self.spectrum.write(':FREQ:STOP 30000000')
            self.spectrum.write(':POW:ATT 10')

            self.spectrum.write(':UNIT:POW DBUV')
            self.spectrum.write(':DISP:WIN:TRAC:Y:DLIN 68')
            self.spectrum.write(':DISP:WIN:TRAC:Y:DLIN:STAT ON')

            self.spectrum.write(':CALC:MARK:AOFF')
            self.spectrum.write(':CALC:MARK1:PEAK:SEAR:MOD MAX')
            self.spectrum.write(':CALC:MARK1:MOD POS')
            self.spectrum.write(':CALC:MARK2:PEAK:SEAR:MOD MAX')
            self.spectrum.write(':CALC:MARK2:MOD POS')
            return 'DONE'
        return 'ERR'
    
    def spectrum_meas_vmax(self):
        if self.spectrum_detected:
            vmax = 0.0
            self.spectrum.write(':CALC:MARK1:MAX:MAX')
            res_vmax = self.spectrum.query('CALC:MARK1:Y?')
            vmax = float('{:.2f}'.format(float(res_vmax)))
            return vmax
        return 'ERR'

