import numpy as np
import cv2

def get_yaw_angle(landmarks):
    model_points = np.array([
        (0.0, 0.0, 0.0),       # Nose tip
        (-30.0, 35.0, -30.0),  # Left eye
        (30.0, 35.0, -30.0),   # Right eye
        (-25.0, -30.0, -30.0), # Left mouth
        (25.0, -30.0, -30.0),  # Right mouth
        (0.0, -75.0, -50.0)    # Chin
    ], dtype="double")

    focal_length = 640
    center = (320, 240)
    camera_matrix = np.array([
        [focal_length, 0, center[0]],
        [0, focal_length, center[1]],
        [0, 0, 1]
    ], dtype="double")

    dist_coeffs = np.zeros((4, 1))
    
    image_points = np.array([
        landmarks[30],  # Nose tip
        landmarks[36],  # Left eye left corner
        landmarks[45],  # Right eye right corner
        landmarks[48],  # Left mouth corner
        landmarks[54],  # Right mouth corner
        landmarks[8]    # Chin
    ], dtype="double")

    success, rotation_vector, translation_vector = cv2.solvePnP(  #translatin:position of head
        model_points, image_points, camera_matrix, dist_coeffs
    )

    rotation_matrix, _ = cv2.Rodrigues(rotation_vector)    #rotation_vector:how the head is rotated 
    angles, _, _, _, _, _ = cv2.RQDecomp3x3(rotation_matrix)
    yaw = angles[1]  
    return yaw
