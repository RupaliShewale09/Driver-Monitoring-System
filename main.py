import cv2
import dlib
from imutils import face_utils
import time
import pygame
import pyttsx3
import numpy as np

from modules.EAR import eye_aspect_ratio 
from modules.MAR import mouth_aspect_ratio
from modules.headpose import get_yaw_angle
from SQL import DrowsinessDatabase 
from notifier2 import send_drowsiness_alerts
from utils import resource_path
    
alarm = resource_path("assets/alarm.wav")
slow_alarm = resource_path("assets/slow_alarm.mp3")

def run_drowsiness_detection(user_email):
    db = DrowsinessDatabase()

    # SOUNDS AND ALERTS --------------------------------------------------------------------------
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')       #getting details of current voice
    engine.setProperty('voice', voices[1].id)   #changes voices 1 for female

    pygame.mixer.init()
    def play_sound(file):
        pygame.mixer.music.load(file)
        pygame.mixer.music.play()

    def stop_sound():
        pygame.mixer.music.stop()
        
    #---------------------------------------------------------------------------------------------
    cap = cv2.VideoCapture(2) 

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        exit()

    detector = dlib.get_frontal_face_detector()   
    predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat") 

    EAR_THRESHOLD = 0.25   #ratio below than 0.25
    CLOSED_EYES_DURATION = 2.0    #Time in seconds to consider drowsines
    HIGH_DURATION = 7.0   #Sec to consider Sleepiness 

    MAR_THRESHOLD = 0.30  #yawning ratio

    YAW_THRESHOLD = 15  # head angle limit for distraction
    DISTRACTION_DURATION = 3.0  # distraction seconds before triggering alert
    
    distraction_start_time = None  # Timer for tracking distraction
    start_time = None
    
    cv2.namedWindow("Drowsiness Detection", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("Drowsiness Detection", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    while True:
        ret, frame = cap.read() 
        if not ret or frame is None:
            print("❌ Error: Could not read frame from webcam.")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector(gray)
        
        status = "Active:)"
        color = (0, 255, 0)

        face_frame = frame.copy()
        
        for face in faces:
            x1, y1, x2, y2 = (face.left(), face.top(), face.right(), face.bottom())
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            
            face_frame = frame.copy()
            
            landmarks = predictor(gray, face)
            landmarks = face_utils.shape_to_np(landmarks)
            
            for n in range(0, 68):
                (x,y) = landmarks[n]
                cv2.circle(frame, (x, y), 1, (255, 255, 255), -1)
            
            # EAR & MAR CALCULATE---------------------------------------------------------------
            # EAR
            left_eye = landmarks[36:42] #Left eye
            right_eye = landmarks[42:48]  #Right eye  

            left_ear = eye_aspect_ratio(left_eye)
            right_ear = eye_aspect_ratio(right_eye)

            avg_ear = (left_ear + right_ear) / 2.0

            cv2.putText(frame, f"EAR: {avg_ear:.2f}", (30, 50),    
                        cv2.FONT_HERSHEY_SIMPLEX, 1,            
                        (0, 0, 0), 2)                          
            # MAR
            mouth = landmarks[60:68]  #Inner lips
            mar = mouth_aspect_ratio(mouth)
            
            cv2.putText(frame, f"MAR: {mar:.2f}", (30, 100),   
                        cv2.FONT_HERSHEY_SIMPLEX, 1,             
                        (0, 0, 0), 2) 
            # Yaw  
            yaw_angle = get_yaw_angle(landmarks)
            cv2.putText(frame, f"Yaw: {yaw_angle:.2f}", (30, 150),
                        cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (0, 0, 0), 2)
            
            # Drosiness Detection-----------------------------------------------------------
            if avg_ear < EAR_THRESHOLD:  
                if start_time is None:
                    start_time = time.time()  #Start the timer
                    
                elapsed_time = time.time() - start_time       #current time - start time

                if elapsed_time >= CLOSED_EYES_DURATION:   #7   
                    if elapsed_time >= HIGH_DURATION:  
                        status = "SLEEPING!!!"
                        color = (255, 0, 0)
                        play_sound(alarm)
                        engine.say("Stop Driving")
                        engine.runAndWait()
                        send_drowsiness_alerts(user_email)
                    else:                               #2
                        status = "DROWSY!!!"
                        color = (0, 0, 255)
                        play_sound(slow_alarm)
                        engine.say("TAKE a BREAK")
                        engine.runAndWait()
            elif mar > MAR_THRESHOLD:        #0.30
                status = "Yawning!!"
                color = (0, 165, 255)  
                engine.say("Please focus on driving!")
                engine.runAndWait()
            elif abs(yaw_angle) > YAW_THRESHOLD:      #15  
                if distraction_start_time is None:
                    distraction_start_time = time.time()
                elif time.time() - distraction_start_time >= DISTRACTION_DURATION:   #3
                    status = "Distracted!"
                    color = (200, 100, 255)
                    engine.say("Distracted!")
                    engine.runAndWait()    
            else:
                start_time = None 
                distraction_start_time = None   
                status = "Active:)"
                color = (0, 255, 0)
                stop_sound() 

            if status != "Active:)":
                db.log_drowsiness(user_email, round(avg_ear, 4), round(mar, 4), round(yaw_angle, 4), status)
            
            cv2.putText(face_frame, status, (100,50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, color, 3)        
            #------------------------------------------------------------------------------- 

        frame_resized = cv2.resize(frame, (640, 480))
        face_frame_resized = cv2.resize(face_frame, (640, 480))
        
        border_color = (0, 0, 0)  
        frame_bordered = cv2.copyMakeBorder(frame_resized, 15, 15, 5, 7, cv2.BORDER_CONSTANT, value=border_color)
        face_frame_bordered = cv2.copyMakeBorder(face_frame_resized, 15, 15, 7, 5, cv2.BORDER_CONSTANT, value=border_color)

        combined_frame = np.hstack((frame_bordered, face_frame_bordered))
        cv2.imshow("Drowsiness Detection", combined_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    db.close_connection()
    cv2.destroyAllWindows()
    
if __name__ == "__main__":
    run_drowsiness_detection()


