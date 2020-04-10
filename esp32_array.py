'''
Device: Grove Pyboard 
Summary: This code sends numbers 0 through 9 from Grove Pyboard to LEGO SPIKE Prime

Tufts Center for Engineering Education and Outreach
Updated on: 01/06/2020
'''
import gc,utime
import micropython
import LPF2

micropython.alloc_emergency_exception_buf(200)

PAYLOAD_LEN = 8

modes = [
# LPF2.mode('LPF2-DETECT',dataType = LPF2.DATA8, raw=[0,10], percent=[0,100], SI=[0,10]),
# LPF2.mode('int8', dataType = LPF2.DATA8),
# LPF2.mode('int16', dataType = LPF2.DATA16),
# LPF2.mode('int32', dataType = LPF2.DATA32),
# LPF2.mode('float', format = '2.1', dataType = LPF2.DATAF),
LPF2.mode('NFC_UID', size=8, dataType=LPF2.DATA8),
# LPF2.mode('NFC_payload', size=32, dataType=LPF2.DATA8),
LPF2.mode('TrxId', size=1, dataType=LPF2.DATA8),
# LPF2.mode('int16_array',size = 4, dataType = LPF2.DATA16),
# LPF2.mode('int32_array',size = 4, dataType = LPF2.DATA32),
# LPF2.mode('float_array',size = 4, format = '2.1', dataType = LPF2.DATAF)
]

# red_led=pyb.LED(1)
# green_led = pyb.LED(2)
# red_led.on()

#lpf2 = LPF2.LPF2(1, 'P1', 'P0', modes, LPF2.SPIKE_Ultrasonic, timer = 4, freq = 5)    # OpenMV
#lpf2 = LPF2.LPF2(3, 'P4', 'P5', modes, LPF2.SPIKE_Ultrasonic, timer = 4, freq = 5)    # OpenMV
lpf2 = LPF2.LPF2(1, 16, 17, modes, LPF2.WeDo_Ultrasonic, timer = 3, freq = 11)    # Grove PyBoard
# use EV3_LPF2 or Prime_LPF2 - also make sure to select the port type on the EV3 to be ev3-uart

lpf2.initialize()

value = 0

startTime = None
# Loop
while True:
     if not lpf2.connected:
          if(startTime != None):
              now = utime.time()
              print("\nSTART TIME: {}  END TIME: {} = {}".format(startTime, now, now - startTime))
              startTime = None
          lpf2.sendTimer.deinit()
          # red_led.on()
          utime.sleep_ms(200)
          lpf2.initialize()
     else:
          # red_led.off()

          if(startTime == None):
              startTime = utime.time()

          value = (value + 1) % 256
          value2 = value
          if(value > 100):
              value2 = value - 100
          payload = b''
          payload += value.to_bytes(1, 'lsb')
          payload += value2.to_bytes(1, 'lsb')
          payload += b'\x00'*(8-len(payload)) # zero-pad our payload to the proper size

          payload2 = payload + b'\x00'*24

          lpf2.load_payload('uInt8', payload,  mode=0)
          # lpf2.load_payload('uInt8', payload2, mode=1)
          lpf2.load_payload('uInt8', value,    mode=1)
          if(value == 0):
              print('')
          print(value, end=' ')

          utime.sleep_ms(200)

