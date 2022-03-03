# visa_instr

Require python-usbtmc modification:
usbtms/usbtmc.py
@@ -68,11 +68,11 @@ USB488_REN_CONTROL      = 160
 USB488_GOTO_LOCAL       = 161
 USB488_LOCAL_LOCKOUT    = 162
 
 USBTMC_HEADER_SIZE = 12
 
-RIGOL_QUIRK_PIDS = [0x04ce, 0x0588]
+RIGOL_QUIRK_PIDS = [0x04ce, 0x0588, 0x0960]
 
 
 def parse_visa_resource_string(resource_string):
     # valid resource strings:
     # USB::1234::5678::INSTR