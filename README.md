# Final Project: Drone Navigation System Based on Human Pose

This repository contains the code and documentation for the project **"Drone Navigation System Based on Human Pose"**. The goal is to implement a drone capable of following a person's pose using computer vision and the MediaPipe library.

## Project Description

The drone's navigation system is built using the following steps:

1. **Human Pose Detection** using MediaPipe and OpenCV.
2. **Pose Processing** to identify the nose landmark and compute horizontal position in the frame.
3. **Drone Control** commands are dynamically sent to the DJI Tello drone to rotate left, right, or remain stationary based on the detected pose.

The project uses the **DJITelloPy** library to interface with the DJI Tello drone, ensuring real-time communication and control.

## Tools and Libraries Used

- **DJITelloPy**: For drone control.
- **MediaPipe**: For human pose detection.
- **OpenCV**: For video capture, processing, and visualization.
- **Python**: Programming language.

## Requirements

To run this project, ensure you have the following libraries installed:

```bash
pip install opencv-python djitellopy mediapipe
```

## Setup Instructions

1. **Connect the Tello Drone** to your hotspot.
2. Clone this repository:

```bash
git clone https://github.com/PachiElCreador/DJI-Tello-Human-Pose-Tracker.git
cd DJI-Tello-Human-Pose-Tracker
```

3. Run the main program:

```bash
python DJItello.py
```

## Files Overview

- `DJItello.py`: Main script for drone pose-based navigation.
- `Control_teclado.py`: Optional script for manual keyboard control of the drone.
- `oracle.py`: Support script for pose detection logic.
- `pruebas.py`: Script for additional testing and debugging.

## Results

The system successfully navigates the drone to track a person's pose, rotating left or right based on nose position. Improvements like PID control for smoother trajectories are suggested for future work.

A demonstration of the project can be viewed here:  
[Project Video](https://youtube.com/shorts/vymavCqRks?si=ttoqMThOYIIWgEiJ)

## Conclusion

This project demonstrates an initial step toward autonomous drone navigation based on pose recognition. It integrates human pose detection and drone control, showcasing the potential for further enhancements like advanced trajectory smoothing using PID control.

## Author

**Óscar Francisco López Carrasco**  
Tecnológico de Monterrey  
December 2023
