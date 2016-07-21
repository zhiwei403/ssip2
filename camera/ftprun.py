import uuid
import ftplib
import hashlib
import httplib
import pytz
import datetime
import urllib
import CameraID

def ftprun(cam_name):
  localtime = datetime.datetime.now(pytz.timezone('Asia/Singapore')).isoformat()
  f = {'ts' : localtime}
  ftp = ftplib.FTP('10.217.137.155','kevin403','S$ip1234')
  ftp.cwd('/var/www/html/image')
  camid = cam_name(cam_name)
  tscam = camid + localtime
  m=hashlib.md5()
  file = open('//home/pi/frame.png','rb')
  
  m.update(tscam)
  dd=m.hexdigest()
  ftp.storbinary('STOR '+dd+'.png', file)
  x = httplib.HTTPConnection('10.217.137.155', 8082)
  x.connect()
  #x.request('GET','/camera/store?cam='+cam_name(cam_name)+ urllib.urlencode(f)+'&fn='+dd)
  x.request('GET','/camera/store?fn='+dd+'&'+urllib.urlencode(f)+'&cam='+cam_name(cam_name))
  y = x.getresponse()
  z=y.read()
  x.close()
  file.close()
  ftp.quit()
  print localtime
#10.217.137.240
