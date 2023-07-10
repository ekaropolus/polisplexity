# import cv2
# import face_recognition


# video_capture = cv2.VideoCapture(0)
def gen_frames():
    pass
    # while True:
    #     # Read the video frame by frame
    #     success, frame = video_capture.read()
    #     if not success:
    #         break
    #     else:
    #         # Convert the frame to grayscale and detect faces
    #         gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #         faces = face_recognition.face_locations(gray)

    #         # Draw rectangles around the faces
    #         for (top, right, bottom, left) in faces:
    #             cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

    #         # Encode the frame as JPEG and return it
    #         ret, buffer = cv2.imencode('.jpg', frame)
    #         frame = buffer.tobytes()
    #         yield (b'--frame\r\n'
    #               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')