import kivy
import time
import numpy as np
from threading import Thread
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.popup import Popup
from kivy.properties import StringProperty
from kivy.graphics.texture import Texture
from picamera import PiCamera
from picamera.array import PiRGBArray
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.config import Config
#Config.set('graphics', 'fullscreen', 'fake')
#Config.write()


iso = 0
exposure = 0 #Microseconds
video_len = 5

open_settings = True

class Settings(FloatLayout):
    iso_set = StringProperty()
    exposure_set = StringProperty()
    videoLen_set = StringProperty()
    
    def save_settings(self):
        global iso, exposure, video_len
        global open_settings
        
        video_len = int(self.videoLen_set)
        
        if self.iso_set == "Auto":
            iso = 0
        else:
            iso = int(self.iso_set)
        
        if self.exposure_set == "Auto":
            exposure = 0
        else:
            exposure = int(self.exposure_set)
            
        open_settings = True

class MyWidget(FloatLayout, BoxLayout):
    
    frame_data = 0
    camera = 0
    num_f = 0
    num_v = 0
    
    isoLabel = StringProperty()
    exposureLabel = StringProperty()
    videoLenLabel = StringProperty()
    
    def update_camera_settings(self):
        global iso, exposure, video_len
        
        self.videoLenLabel = str(video_len)
        
        if iso != 0:
            self.camera.iso = iso
            self.isoLabel = str(iso)
        else:
            self.isoLabel = "Auto"
            self.camera.iso = iso
            
        if exposure != 0:
            self.camera.shutter_speed = exposure
            self.exposureLabel = str(exposure)
        else:
            self.exposureLabel = "Auto"
            self.camera.shutter_speed = exposure
    
    def update_texture(self, frame):
        global open_settings
        frame = self.frame_data
        buffer = frame.tostring()
        texture1 = Texture.create(size=(600, 400), colorfmt="rgb")
        texture1.blit_buffer(buffer, colorfmt='rgb', bufferfmt='ubyte')
        
        self.image_camera.texture = texture1
        
        if open_settings == True:
            self.update_camera_settings()
            open_settings = False
            
    def update_kivy(self):
        Clock.schedule_once(self.update_texture)
    
    def camera_process(self):
        camera = PiCamera()
        self.camera = camera
        camera.resolution = (600, 400)
        
        rawcapture = PiRGBArray(camera)
        
        for frame in camera.capture_continuous(rawcapture, format="rgb", use_video_port=True):
            frame_array = rawcapture.array
            self.frame_data = frame_array
            self.update_kivy()
            
            rawcapture.truncate(0)
            
    def thread_camera(self):
        camera_thread = Thread(name="camera", target=self.camera_process)
        camera_thread.setDaemon(True)
        camera_thread.start()

    def foto_process(self):
        self.camera.start_preview()
        time.sleep(2)
        self.camera.capture('image_#%s.png' % self.num_f)
        self.camera.stop_preview()
        self.num_f += 1
        
    def thread_foto(self):
        foto_thread = Thread(name="camera_foto", target=self.foto_process)
        foto_thread.setDaemon(True)
        foto_thread.start()
    
    def record_process(self):
        global video_len
        self.camera.start_recording('my_video_%s.h264' % self.num_v)
        time.sleep(video_len)
        self.camera.stop_recording()
        self.num_v += 1
        
    def thread_record(self):
        record_thread = Thread(name="camera_record", target=self.record_process)
        record_thread.setDaemon(True)
        record_thread.start()
    
    def settings(self):
        show_popup()
    
    
class MyApp(App):
    def build(self):
        return MyWidget()
    

def show_popup():
    show = Settings() # Create a new instance of the P class 

    popupWindow = Popup(title="Camera Settings", content=show, size_hint=(None,None),size=(400,400)) 
    # Create the popup window

    popupWindow.open() # show the popup




if __name__ == '__main__':
    MyApp().run()