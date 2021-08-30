from visa_device import PyVISA_Device

def main():
    # mymx5060 = mx5060(9600, 8, 1, True, False, False, 0.5)

    # if mymx5060.portname() is None:
    #     print("MX5060: Error")
    # else:
    #     print("MX5060: " + mymx5060.portname()) 

    # mydsa705= dsa705()
    # try:
    #     mydsa705.instr.open()
    # except Exception:
    #     raise NotImplementedError()
    
    # print(mydsa705.identification())
    # mydsa705.configure()
    # print(mydsa705.meas_max())
    # print(mydsa705.measure())
    # print(mydsa705.meas_max())
    # del mydsa705

    myvisa = PyVISA_Device()
    print(myvisa.resources)

    print(myvisa.scope_ident)
    print(myvisa.spectrum_ident)
    print(myvisa.multimeter_ident)
    
    print(myvisa.scope_config_riple())
    print(myvisa.spectrum_config())
    print(myvisa.multimeter_config_dc())

    print(myvisa.scope_meas_vmax())
    print(myvisa.scope_meas_vmin())
    print(myvisa.spectrum_meas_vmax())
    print(myvisa.multimeter_measure())

    myvisa.scope_close()
    print(myvisa.spectrum_meas_vmax())


if __name__ == "__main__":
    main()