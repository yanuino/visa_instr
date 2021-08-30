from scpi_device import Scpi_Device

class mx5060(Scpi_Device):
    def __init__(
        self,
        baudrate=4800,
        bytesize=8,
        stopbits=1,
        xonxoff=True,
        rtscts=False,
        dsrdtr=False,
        timeout_rw=0.5):

        self.models = ['MX5060']

        super().__init__(
            baudrate,
            bytesize,
            stopbits,
            xonxoff,
            rtscts,
            dsrdtr,
            timeout_rw)

        super().autodetect(self.models)
    
    def portname(self):
        return self.port_name

    def configure(self):
        # configuring volt dc measurement
        res = self.send_command('*CLS')
        res += self.send_command('FUNC \"VOLT\"')
        ### if most problems, insert error management (SYST:ERR? => Noerror | SettinConflict ...)
        res += self.send_command('INP:COUP DC')
        res += self.send_command('RANG:AUTO 0')
        res += self.send_command('RANG 10.0')
        res += self.send_command('FILT 0')
        return res
    
    def measure(self):
        res = self.send_command('READ?')
        return [ 'VOLT_DC', res, 'V']

    def local(self):
        res = self.send_command('SYST:LOC')
        return res


