
from djitellopy import Tello
import cv2
import time
h, w = 0, 0

# Inicializar el dron Tello
tello = Tello()
tello.connect()
tello.streamon()

# Configurar la cámara y resolución
width, height = 320, 240
#tello.set_video_resolution(f"{w}x{h}")

# Cargar el clasificador de Haar para detección de rostros
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Variables para el seguimiento del cuerpo
target_center_y = h // 3  # 33% del frame vertical
yaw_speed = 30  # Velocidad de giro del dron
face_target_distance = 120  # Distancia objetivo entre el rostro y el dron
target_height = 10  # Altura objetivo del dron

# Función para elevarse a aproximadamente 2 metros
def takeoff_and_hover():
    tello.takeoff()
    time.sleep(5)
    tello.move_up(target_height)  # Altura objetivo del dron

# Función para buscar un cuerpo humano
def search_for_human(myframe):
    gray = cv2.cvtColor(myframe, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
    
    if len(faces) > 0:
        return faces[0]  # Devolver las coordenadas del primer rostro detectado
    else:
        return None

# Función para seguir al cuerpo humano
def follow_human(face_coordinates):
    global target_center_y, yaw_speed, face_target_distance, target_height

    x, y, w, h = face_coordinates
    face_center_y = y + h // 2
    face_center_x = x + w // 2

    # Calcular la diferencia entre el centro del rostro y el centro deseado
    y_error = target_center_y - face_center_y

    # Calcular la diferencia en la distancia entre el dron y el rostro
    distance_error = face_target_distance - w

    # Ajustar la orientación del dron en función del error en el eje Y
    if y_error > 10:
        tello.rotate_counter_clockwise(yaw_speed)
    elif y_error < -10:
        tello.rotate_clockwise(yaw_speed)
    else:
        tello.rotate_clockwise(0)  # Detener la rotación

    # Ajustar la distancia del dron al rostro
    if distance_error > 10:
        tello.move_back(distance_error // 2)  # Ajustar la velocidad de movimiento hacia atrás
    elif distance_error < -10:
        tello.move_forward(abs(distance_error // 2))  # Ajustar la velocidad de movimiento hacia adelante

# Función principal
def main():
    try:
        takeoff_and_hover()

        while True:
            frame_read = tello.get_frame_read()
            myFrame = frame_read.frame
            img = cv2.resize(myFrame, (width, height))

            
            # Muestra el video en una ventana
            cv2.imshow("Video", img)
            cv2.waitKey(25)

            # 
            face_coordinates = search_for_human(img)

            if face_coordinates is not None:
                follow_human(face_coordinates)
            else:
                # Si no se encuentra un rostro, rodar a velocidad media
                tello.rotate_clockwise(yaw_speed)

            # Rompe el bucle si se presiona la tecla 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    finally:
        # Aterriza el dron al salir del programa
        tello.land()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
