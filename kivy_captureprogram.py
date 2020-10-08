import kivy
import time
import numpy as np
from threading import Thread
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.graphics.texture import Texture
from picamera import PiCamera
from picamera.array import PiRGBArray
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.config import Config
Config.set('graphics', 'fullscreen', 'fake')
Config.write()

iso = 0
open_settings = False

class Settings(FloatLayout):
    
    def save_settings(self):
        global iso
        global open_settings
        iso = 100
        open_settings = True

class MyWidget(FloatLayout, BoxLayout):
    
    frame_data = 0
    camera = 0
    num = 0
    
    def update_camera_settings(self):
        global iso
        self.camera.iso = iso
    
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
        self.camera.capture('image#%s.png' % self.num)
        self.camera.stop_preview()
        self.num += 1
        
    def thread_foto(self):
        foto_thread = Thread(name="camera_foto", target=self.foto_process)
        foto_thread.setDaemon(True)
        foto_thread.start()
    
    def record_process(self):
        self.camera.start_recording('my_video.h264')
        time.sleep(5)
        self.camera.stop_recording()
        
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