import cv2
from datetime import datetime

class Camera:
    ''' A class that captures an image using the connected camera on the device'''
    def __init__(self, camera_idx = 0):
        self._camera = camera_idx
    
    def capture_image(self, num_imgs = 1):
        '''Captures a given number of images. By default, it captures only one image'''
        camera = cv2.VideoCapture(self._camera)
        for i in range(num_imgs):
            unused_value, image = camera.read()
            now = datetime.now()
            timestamp = now.strftime("%m_%d_%Y, %H_%M_%S")
            print(timestamp)
            cv2.imwrite(f'images/captured/{timestamp}.jpg', image)
        del(camera)
    
    def set_camera(self, camera_idx):
        '''Used to change the camera to be used when capturing images. 0 is the default (i.e. webcam)'''
        self._camera = camera_idx
    

if __name__ == "__main__":
    camera = Camera()
    camera.capture_image(1)
    
    


