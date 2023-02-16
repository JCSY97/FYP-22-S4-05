import cv2
from django.http import HttpResponse, StreamingHttpResponse, request
from django.shortcuts import render
from flask import Flask, render_template, Response

from index.views.facialRec import FR_class

from rest_framework.decorators import api_view

from django.http import JsonResponse


import base64

import os
import face_recognition
import numpy as np

from index.models import Employee, Role, WorkSchedule
from datetime import date,datetime, timedelta

app = Flask(__name__)

#FR = FR_class("siamesemodelv2.h5")




# get list of face encoding when server starts
verify_file_path = os.path.join("media", "verify")

known_face_encodings = []
known_face = []


for person in os.listdir(verify_file_path):
    # skip verify_test
    if person == "verify_test":
        continue

    image_path = os.path.join(verify_file_path, person)

    # add name to list of known_faces
    known_face.append(person)
    print(str(image_path) + " has been added to encoded_face_list")
    
    # add encoded image to list of known face encoding
    # get first pic of each folder
    img_of_person_file_path = os.path.join(image_path ,os.listdir(image_path)[0])
    img_of_person = face_recognition.load_image_file(img_of_person_file_path)
    img_of_person_encoding = face_recognition.face_encodings(img_of_person)[0]
    
    known_face_encodings.append(img_of_person_encoding)

print(known_face)
print(len(known_face_encodings))




# class VideoCamera(object):
#     def __init__(self):
#         # Using OpenCV to capture from device 0. If you have trouble capturing
#         # from a webcam, comment the line below out and use a video file
#         # instead.
#         self.video = cv2.VideoCapture(0)
#         self.video.set(3, 640)
#         self.video.set(4, 480)

#     def __del__(self):
#         self.video.release()

#     def get_frame(self):

#         cascPath = "static/assets/js/haarcascade_frontalface_default.xml"
#         faceCascade = cv2.CascadeClassifier(cascPath)
#         success, image = self.video.read()
#         image = cv2.flip(image, 1)
#         # We are using Motion JPEG, but OpenCV defaults to capture raw images,
#         # so we must encode it into JPEG in order to correctly display the
#         # video stream.
#         gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#         #imgname = os.path.join(Image_PATH,f'{str(uuid.uuid1())}.jpg')
#         faces = faceCascade.detectMultiScale(gray,
#                                              scaleFactor=1.2,
#                                              minNeighbors=5,
#                                              minSize=(20, 20))

#         for (x, y, w, h) in faces:

#             cv2.rectangle(image, (x, y), (x + w, y + h), (94, 183, 3), 2)
#             # cv2.putText(image, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2, cv2.LINE_AA)
#         ret, jpeg = cv2.imencode('.jpg', image)
#         return jpeg.tobytes()


@app.route('/')
def index(request):
    if request.method == 'POST':
        try:
            frame_ = request.POST.get('image')
            frame_ = str(frame_)
            data = frame_.replace('data:image/jpeg;base64,', '')
            data = data.replace(' ', '+')
            imgdata = base64.b64decode(data)


            filename = 'media/verify/verify_test/inputImage.jpg'
            with open(filename, 'wb') as f:
                f.write(imgdata)

            input_face = face_recognition.load_image_file(filename)
            face_locations = face_recognition.face_locations(input_face)
        

            if len(face_locations) == 1:
                # compare with known faces
                # encode input face
                input_face_encoding = face_recognition.face_encodings(input_face)[0]
                face_distances = face_recognition.face_distance(known_face_encodings, input_face_encoding)
                best_match_index = np.argmin(face_distances) 




                # face detected
                if face_distances[best_match_index] < 0.4:
                    print("employee " + str(known_face[best_match_index]) + " has detected")


                    # check if this emp id is in database
                    currentDate = datetime.now().strftime("%Y-%m-%d")
                    currentTime =  datetime.now().strftime('%H:%M:%S')

                    # check if this person is in EMPLOYEE table
                    if Employee.objects.filter(Employee_ID=known_face[best_match_index]):
                        # check if this person is in WORKSCHEDULE table
                        EMPID = known_face[best_match_index]
                        AttenIntime =WorkSchedule.objects.filter(Employee_ID=EMPID,StartDate=currentDate)
                        if AttenIntime.exists():
                            if AttenIntime[0].InTime is None:
                                AttenIntime[0].InTime =currentTime
                                AttenIntime[0].save()
                            else:
                                t1 = AttenIntime[0].InTime
                                t2 = datetime.strptime(currentTime, "%H:%M:%S")

                                # get difference
                                delta = t2 - t1
                                # time difference in seconds
                                if (delta.total_seconds() / 60 / 60)>=1:
                                    AttenIntime[0].OutTime =currentTime
                                    AttenIntime[0].save()

                                










                        # clock in
                        if WorkSchedule.objects.filter(Employee_ID=known_face[best_match_index], StartDate=currentDate, InTime__isnull==True):
                            today_work_schedule = WorkSchedule.objects.get(Employee_ID=known_face[best_match_index], StartDate=currentDate)

                            today_work_schedule.InTime = currentTime

                        # clock out
                        elif WorkSchedule.objects.filter(Employee_ID=known_face[best_match_index], StartDate=currentDate, InTime__isnull==False):
                            if currentTime > InTime+1hour










                else:
                    print("face not in database")
            elif len(face_locations) > 1:
                print("more than one face detected")

            else:
                print("no face has been detected")





            # delete photo from verifyTest after this loop
            os.remove(filename)


            #return JsonResponse({"valid": str(compare_verified)}, status=200)
            return JsonResponse({"valid": "hello"}, status=200)

        except Exception as e:
            print(e)

    return render(request, 'index/camera.html')





# def gen(camera):
#     while True:
#         frame = camera.get_frame()
#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/video_feed')
def video_feed(request):
    # return StreamingHttpResponse(gen(VideoCamera()), content_type='multipart/x-mixed-replace; boundary=frame')
    return StreamingHttpResponse(gen(VideoCamera()), content_type='multipart/x-mixed-replace; boundary=frame')


# @api_view(['GET'])
# def return_verified(request):

#     return reponse(verified)


if __name__ == 'main':
    app.run()
