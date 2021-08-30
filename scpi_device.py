import serial
import serial.tools.list_ports
import ast
import sys
import time

class Scpi_Device(object):
    def __init__(
        self,
        baudrate,
        bytesize,
        stopbits,
        xonxoff,
        rtscts,
        dsrdtr,
        timeout_rw):

        self.serial_object = None
        self.port_name = None
        self.baudrate = baudrate
        self.bytesize = bytesize
        self.stopbits = stopbits
        self.xonxoff = xonxoff
        self.rtscts = rtscts
        self.dsrdtr = dsrdtr
        self.timeout_rw = timeout_rw
        self.ident = None

    def __comports(self):
        return [port.device for port in serial.tools.list_ports.comports()]

    def open(self, port=None):
        if port is None:
            port = self.port_name

        # open port
        try:

            # Create serial object
            self.serial_object = serial.Serial()
            self.serial_object.port = port
            self.serial_object.baudrate = self.baudrate
            self.serial_object.timeout = self.timeout_rw             #non-block read
            self.serial_object.writeTimeout = self.timeout_rw
            self.serial_object.bytesize = self.bytesize              #serial.EIGHTBITS
            self.serial_object.parity = serial.PARITY_NONE              #set parity check: no parity
            self.serial_object.stopbits = self.stopbits              
            self.serial_object.xonxoff = self.xonxoff        
            self.serial_object.rtscts = self.rtscts         
            self.serial_object.dsrdtr = self.dsrdtr


            self.serial_object.open()
            time.sleep(0.5)

        except Exception as e:
            return "KO : Exception open serial port : " + sys.exc_info()[-1].tb_frame.f_code.co_filename + "\n" + "error on line : " + str(sys.exc_info()[-1].tb_lineno) + "\n" + str(e)

        return 'OK'


    def close(self):

        try:
            if self.serial_object.isOpen():
                self.serial_object.close()
        except Exception as e:
            return "KO : Exception close serial port : " + sys.exc_info()[-1].tb_frame.f_code.co_filename + "\n" + "error on line : " + str(sys.exc_info()[-1].tb_lineno) + "\n" + str(e)

        return "OK"

    def identification(self, p=None):
        command = '*IDN?'
        self.open(p)
        res = self.send_command(command)
        self.close()
        
        return res

    def autodetect(self, models):
        port_list = self.__comports()

        for p in port_list:
            print("<<< SCPI DEVICE - Trying port " + p + " >>>")
            res = self.identification(p)
            for model in models:
                if model in res:
                    self.port_name = p
                    self.ident = res
                    break

        time.sleep(0.3)

    def __write(self, command):

        if self.serial_object == None:
            return "KO : __write serial_object is not defined, please call open_serial_port function "

        if self.serial_object.isOpen():
            try:
                self.serial_object.flushInput() #flush input buffer, discarding all its contents
                self.serial_object.flushOutput()#flush output buffer, aborting current output and discard all that is in buffer

                self.serial_object.write(command + '\n')

                return "OK"

            except Exception as e:
                return "KO : __write Exception communicating : " + sys.exc_info()[-1].tb_frame.f_code.co_filename + "\n" + "error on line : " + str(sys.exc_info()[-1].tb_lineno) + "\n" + str(e)
        else:
            return "KO : __write Exception can not open serial port : " + self.serial_object.port


    def __read(self):

        if self.serial_object == None:
            return "KO : serial_object is not defined, please call open_serial_port function "


        if self.serial_object.isOpen():
            try:
                res = self.serial_object.readline()
                return res

            except Exception as e:
                return "KO : __read Exception communicating : " + sys.exc_info()[-1].tb_frame.f_code.co_filename + "\n" + "error on line : " + str(sys.exc_info()[-1].tb_lineno) + "\n" + str(e)
        else:
            return "KO : __read Exception can not open serial port : " + self.serial_object.port


    def __read_to_line(self, line_to_read):

        if self.serial_object == None:
            return "KO : serial_object is not defined, please call open_serial_port function "


        if self.serial_object.isOpen():
            try:
                res = ""
                i = 0
                while i < int(line_to_read):
                    res = res + self.serial_object.readline()
                    i = i + 1

                return res

            except Exception as e:
                return "KO : __read Exception communicating : " + sys.exc_info()[-1].tb_frame.f_code.co_filename + "\n" + "error on line : " + str(sys.exc_info()[-1].tb_lineno) + "\n" + str(e)
        else:
            return "KO : __read Exception can not open serial port : " + self.serial_object.port

    def send_command(self, command, lines_to_read=1):
        RETRY = 2
        for i in range(RETRY):
            res_w= self.__write(command)
            time.sleep(1)

            res_r = self.__read_to_line(1)

            if res_w[0:2] == "OK" and res_r[0:2] != "KO":
                return res_r

            time.sleep(0.5)

        return res_w + ' ' + res_r

        
        

