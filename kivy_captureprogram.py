import kivy
import time
from threading import Thread
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics.texture import Texture
from picamera import PiCamera
from picamera.array import PiRGBArray
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.config import Config
Config.set('graphics', 'fullscreen', 'fake')
Config.write()


class MyWidget(FloatLayout):
    
    frame_data = 0
    
    def update_texture(self, frame):
        frame = self.frame_data
        buffer = frame.tostring()
        texture1 = Texture.create(size=(600, 400), colorfmt="rgb")
        texture1.blit_buffer(buffer, colorfmt='rgb', bufferfmt='ubyte')
        
        self.image_camera.texture = texture1
    
    def update_kivy(self):
        Clock.schedule_once(self.update_texture)
    
    def camera_process(self):
        camera = PiCamera()
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

    
class MyApp(App):
    def build(self):
        return MyWidget()
    


if __name__ == '__main__':
    MyApp().run()