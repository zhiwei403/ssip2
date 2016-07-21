import gi
gi.require_version('Gst', '1.0')
from gi.repository import GObject #,Gtk
from gi.repository import Gst as gst
import time


class TakePhoto:

    def __init__(self):
        GObject.threads_init()
        gst.init(None)
        self.pipeline = gst.Pipeline()
        self.video_source = gst.ElementFactory.make('v4l2src', 'video_source')
        self.video_source.set_property("num-buffers",1)
        self.videoconvert = gst.ElementFactory.make('videoconvert', 'videoconvert')
        self.clock = gst.ElementFactory.make('clockoverlay', 'clock')
        self.timer= gst.ElementFactory.make('timeoverlay','timer')
        self.videorate = gst.ElementFactory.make('videorate', 'videorate')
        self.sconvert = gst.ElementFactory.make('videoconvert', 'sconvert')
        self.png = gst.ElementFactory.make('pngenc', 'png')
        self.multi_sink = gst.ElementFactory.make('multifilesink', 'multi_sink')
        self.multi_sink_pad = self.multi_sink.get_static_pad('sink')
        self.probe_id = self.multi_sink_pad.add_probe(gst.PadProbeType.EVENT_UPSTREAM,self.probe_callback)
        
        self.caps = gst.caps_from_string("video/x-raw,format=RGB,width=800,height=600,framerate=5/1")
        self.timer.set_property('valignment','bottom')
        self.timer.set_property('halignment','right')
        self.clock.set_property('time-format','%Y/%m/%d %H:%M:%S')
        self.clock.set_property('valignment','bottom')
        self.caps1 = gst.caps_from_string("video/x-raw,framerate=1/1")
        self.png.set_property('snapshot',True)
        #self.png.set_property('idct-method',1)
        self.multi_sink.set_property('location','/home/pi/frame.png')
        self.filter = gst.ElementFactory.make("capsfilter", "filter")
        self.filter.set_property("caps", self.caps)
        self.filter1 = gst.ElementFactory.make("capsfilter", "filter1")
        self.filter1.set_property("caps", self.caps1)

        self.pipeline.add(self.video_source)
        self.pipeline.add(self.videoconvert)
        self.pipeline.add(self.timer)
        self.pipeline.add(self.clock)
        self.pipeline.add(self.filter)
        self.pipeline.add(self.videorate)
        self.pipeline.add(self.filter1)
        self.pipeline.add(self.sconvert)
        self.pipeline.add(self.png)
        self.pipeline.add(self.multi_sink)

        self.video_source.link(self.filter)
        self.filter.link(self.videoconvert)
        self.videoconvert.link(self.timer)
        self.timer.link(self.clock)
        self.clock.link(self.videorate)
        self.videorate.link(self.filter1)
        self.filter1.link(self.sconvert)
        self.sconvert.link(self.png)
        self.png.link(self.multi_sink)
        #self.pipeline.set_state(gst.State.PLAYING)

    def probe_callback(self,multi_sink_pad,info):
        info_event = info.get_event()
        info_structure = info_event.get_structure()
        #do_something_with_this_info
        return gst.PadProbeReturn.PASS    
        
    def take_photo(self): #this is reusable
        bus = self.pipeline.get_bus()
        self.pipeline.set_state(gst.State.PLAYING)
        print "Capture started"
        msg = bus.timed_pop_filtered(gst.CLOCK_TIME_NONE,gst.MessageType.ERROR | gst.MessageType.EOS)
        print msg
        
        self.pipeline.set_state(gst.State.NULL)



