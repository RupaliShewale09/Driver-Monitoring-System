from scipy.spatial import distance as dist

def eye_aspect_ratio(eye):
    A = dist.euclidean(eye[1], eye[5])     # p2 p6   
    B = dist.euclidean(eye[2], eye[4])     # p3 p5
    C = dist.euclidean(eye[0], eye[3])     # p1 p4

    ear = (A + B) / (2.0 * C)
    return ear
