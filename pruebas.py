import cv2
import cv2
import threading
import time
from djitellopy import Tello
import mediapipe as mp


# Inicializar el dron Tello
tello = Tello()

# Conectar al dron
tello.connect()

#Despegue
tello.takeoff()
time.sleep(2)

# Velocidad de giro del dron
yaw_speed = 20  

# Iniciar la transmisión de la cámara
tello.streamon()

#Detector de pose
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
    

    
#Bucle
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while True:
        frame = tello.get_frame_read().frame

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
            if cx < centro - 90:
                # Move to the left
                print("Left")
                tello.rotate_clockwise(yaw_speed)
            elif cx > centro + 90:
                # Move to the right
                print("Right")
                tello.rotate_counter_clockwise(yaw_speed)
            elif cx == centro:
                # Stop the servo
                print("Stop")
                tello.rotate_clockwise(0)  # Detener la rotación

        cv2.imshow("Camara", annotated_frame)
        t = cv2.waitKey(1)
        if t == 27:
            break

# Detener la transmisión y cerrar la ventana al salir
tello.streamoff()
cv2.destroyAllWindows()

#Aterrizaje
time.sleep(2)
tello.land()

# Desconectar del dron
tello.disconnect()
