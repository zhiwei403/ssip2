import camera
import CameraID
import ftprun


def run(cam_name):
    myserial = CameraID.cam_name(cam_name)
    #print "Local current time :",localtime1(localtime1)
    print myserial
    print camera.take_photo()
      #print "Local current time :",localtime1(localtime1)
    print ftprun.ftprun(cam_name)
