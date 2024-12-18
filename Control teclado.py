#Librerias
import cv2
import mediapipe as mp
import serial

#configuración del puerto serial
#com = serial.Serial("COM10", 9600, write_timeout=10)
r = 'r'
l = 'l'
s = 's'

#Detector de pose
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

#Videocaptura
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

#Bucle
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while True:
        ret, frame = cap.read()

        # Espejo al frame
        frame = cv2.flip(frame, 1)

        # Conversión de formato de color
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Función para la pose
        results = pose.process(rgb)

        # Dibujamos la pose en el video
        annotated_frame = frame.copy()
        mp_drawing.draw_landmarks(annotated_frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        # Si detecta la pose:
        if results.pose_landmarks:
            # Cordenadas del centro de la pose
            cx = int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE].x * frame.shape[1])
            cy = int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE].y * frame.shape[0])

            # Mostrar un punto en el centro
            cv2.circle(annotated_frame, (cx, cy), 3, (0, 0, 255), cv2.FILLED)
            cv2.line(annotated_frame, (cx, 0), (cx, frame.shape[0]), (0, 0, 255), 2)

            # Mover el servo
            centro = frame.shape[1] // 2  
            if cx < centro - 70:
                # Move to the left
                print("Left")
                #com.write(l.encode('ascii'))
            elif cx > centro + 70:
                # Move to the right
                print("Right")
                #com.write(r.encode('ascii'))
            elif cx == centro:
                # Stop the servo
                print("Stop")
                #com.write(s.encode('ascii'))

        cv2.imshow("Camara", annotated_frame)
        t = cv2.waitKey(1)
        if t == 27:
            break

cap.release()
cv2.destroyAllWindows()