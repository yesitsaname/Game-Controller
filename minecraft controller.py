# -*- coding: utf-8 -*-
"""
Created on Tue Aug 22 19:54:59 2023

@author: LENOVO
"""

import cv2
import mediapipe as mp
import pyautogui
import keyboard

cam = cv2.VideoCapture(0)
face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)

cap = cv2.VideoCapture(0)
hand_detect = mp.solutions.hands.Hands()
drawing = mp.solutions.drawing_utils
screen_width, screen_height = pyautogui.size()     #get size of my screen to scale

index_y = 0 # these values will later change when in the for loop
thumb_y = 0
middle_y = 0


while True:
    _,frame = cam.read()
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    frame_height, frame_width, _ = frame.shape  #takes values from shape. channel no not needed
    output = face_mesh.process(rgb_frame)
    landmark_points = output.multi_face_landmarks
    #print(landmark_points)

    if landmark_points :
        landmarks = landmark_points[0].landmark
        for id, landmark in enumerate(landmarks[474 : 478 ]) :  #this range selects landmarks for eyes only
            x = int(landmark.x *frame_width)
            y = int(landmark.y *frame_height)
            cv2.circle(frame,(x,y),3, (0,254,69), 1)

            if id == 1 :
                if y <150 :
                    keyboard.press("w")
                if y > 150 :
                    keyboard.release("w")
                if y >350 :
                    keyboard.press("s")
                if y < 350 :
                    keyboard.release("s")

                if x <250 :
                    keyboard.press("a")
                if x > 250 :
                    keyboard.release("a")
                if x >450 :
                    keyboard.press("d")
                if x < 450 :
                    keyboard.release("d")


            print(x,y)
            
    #frame2 = cv2.flip(frame,1)
    frame2 = frame

    frame_height, frame_width, _ = frame2.shape  #takes values from shape. channel no not needed

    rgb_frame = cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB)

    output = hand_detect.process(rgb_frame)
    hands = output.multi_hand_landmarks
    if hands :
        for hand in hands :
            drawing.draw_landmarks(frame, hand)
            landmarks = hand.landmark
            for id, landmark in enumerate(landmarks) :
                hx = int(landmark.x*frame_width)
                hy = int(landmark.y*frame_height)
                #print(x,y)
                if id == 8 :  #landmark for index finger
                    cv2.circle(img=frame,center=(hx,hy), radius = 10, color= (0,255,255))
                    index_x = screen_width/frame_width*hx
                    index_y = screen_height/frame_height*hy  # added value /3 for stability
                    pyautogui.moveTo(index_x,index_y)
                if id == 12:  # landmark for middle finger
                    cv2.circle(img=frame, center=(hx, hy), radius=10, color=(0, 190, 187))
                    middle_x = screen_width / frame_width * hx
                    middle_y = screen_height / frame_height * hy
                if id == 4 :  #landmark for thumb finger
                    cv2.circle(img=frame,center=(hx,hy), radius = 10, color= (0,234,255))
                    thumb_x = screen_width/frame_width*hx
                    thumb_y = screen_height/frame_height*hy

                    if abs(middle_y - thumb_y) <40 :
                        print('click')
                        pyautogui.click()
                        pyautogui.sleep(1)  # will click at intervals of 1s
    cv2.imshow("eye contol ", frame)
    k = cv2.waitKey(25)
    if k == ord("q"):
        break
    '''cv2.imshow('Virtual Mouse', frame)
    k = cv2.waitKey(25)
    if k == ord("q") :
        break'''
cap.release()
cam.release()
cv2.destroyAllWindows()