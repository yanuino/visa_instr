""" If you cannot access your device without running your script as root,
then you may need to create a udev rule to properly set the permissions of the device.
First, connect your device and run lsusb. Find the vendor and product IDs.
Then, create a file /etc/udev/rules.d/usbtmc.rules with the following content:

# USBTMC instruments
# Rigol DSA705
SUBSYSTEMS=="usb", ACTION=="add", ATTRS{idVendor}=="1ab1", ATTRS{idProduct}=="0960", GROUP="usbtmc", MODE="0660

You will also need to create the usbtmc group and add yourself to it or substitute another group of your choosing """

import usbtmc

class Usbtmc_Device(object):
    def __init__(self, idVendor = None, idProduct = None):
        self.idVendor = idVendor
        self.idProduct = idProduct
        self.instr = None

        if idVendor is not None and idProduct is not None:
            try:
                self.instr = usbtmc.Instrument(idVendor, idProduct)
            except Exception:
                raise NotImplementedError()

    def __devices(self):
        return usbtmc.list_devices()

    def identification(self):
        command = "*IDN?"
        res = self.instr.ask(command)
        return res

    def autodetect(self, models):
        ## TODO: 
        ## raw = self.__devices()
        ## extracting idVendor and idProduct tupple
        ## calling self.identification for each tupple
        ## comparing result with models
        ## 
        pass
    

