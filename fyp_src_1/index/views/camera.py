import cv2
from django.http import HttpResponse , StreamingHttpResponse, request
from django.shortcuts import render
from flask import Flask, render_template,Response
app = Flask(__name__)
class VideoCamera(object):
    def __init__(self):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
        self.video = cv2.VideoCapture(0)
        self.video.set(3, 640)
        self.video.set(4, 480)
    
    def __del__(self):
        self.video.release()
    
    def get_frame(self):
        
        cascPath = "static/assets/js/haarcascade_frontalface_default.xml"
        faceCascade = cv2.CascadeClassifier(cascPath)
        success, image = self.video.read()
        image =  cv2.flip(image,1)
        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        #imgname = os.path.join(Image_PATH,f'{str(uuid.uuid1())}.jpg')
        faces = faceCascade.detectMultiScale(gray, 
            scaleFactor=1.2,
            minNeighbors=5,     
            minSize=(20, 20))

        for (x, y, w, h) in faces:

            cv2.rectangle(image, (x, y), (x + w, y + h), (94, 183, 3), 2)
            # cv2.putText(image, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2, cv2.LINE_AA)
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

@app.route('/')
def index(request):
    return render(request, 'index/camera.html')


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed(request):
    # return StreamingHttpResponse(gen(VideoCamera()), content_type='multipart/x-mixed-replace; boundary=frame')
    return StreamingHttpResponse (gen(VideoCamera()), content_type='multipart/x-mixed-replace; boundary=frame')


if __name__ == 'main':
    app.run()