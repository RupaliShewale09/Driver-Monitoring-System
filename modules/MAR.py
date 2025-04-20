from scipy.spatial import distance as dist

def mouth_aspect_ratio(mouth):
    A = dist.euclidean(mouth[1], mouth[7])  # P2 - P8 (61 - 67)
    B = dist.euclidean(mouth[2], mouth[6])  # P3 - P7 (62 - 66)
    C = dist.euclidean(mouth[3], mouth[5])  # P4 - P6 (63 - 65)
    D = dist.euclidean(mouth[0], mouth[4])  # P1 - P5 (60 - 64)

    MAR = (A + B + C) / (3.0 * D)
    return MAR
