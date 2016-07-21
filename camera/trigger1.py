import RPi.GPIO as GPIO
import camera
import CameraID
import select
c=camera.TakePhoto()


pin_base = '/sys/class/gpio/gpio23/'

def write_once(path, value):
     f = open(path, 'w')
     f.write(value)
     f.close()
     return

f = open(pin_base + 'value', 'r')
write_once(pin_base + 'direction', 'in')
write_once(pin_base + 'edge', 'both')

po = select.poll()
po.register(f, select.POLLPRI)

while 1:
     events = po.poll(6000)
     f.seek(0)
     state_last = f.read()
     if len(events) == 0:
          print ('timeout')
     else:
          print 'Val: %s' % state_last
          if (state_last[0] == '1' ):
                #GPIO.output(23,GPIO.HIGH)    
                print c.take_photo()
                #GPIO.output(23,GPIO.HIGH)  
                print CameraID.run()
          
