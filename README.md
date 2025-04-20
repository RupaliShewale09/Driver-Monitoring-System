# 🚗 DriCare360 – Driver Monitoring System

**DriCare360** is a smart driver safety solution built to monitor a driver’s alertness and detect early signs of drowsiness using facial landmark analysis. The system leverages a webcam to analyze **eye closure (EAR)**, **yawning (MAR)**, and **head tilts (yaw angle)** in real time. If signs of drowsiness are detected, DriCare360 initiates **audio alerts** and **sends email notifications** to the driver’s emergency contact.

---

## 🧠 Key Highlights

- ✅ Built using **Streamlit** for a user-friendly interface
- ✅ Analyzes live webcam feed with facial landmark detection
- ✅ Detects closed eyes, yawns, and head tilts using EAR, MAR, and yaw
- ✅ Sends **automatic alerts** via email to prevent accidents
- ✅ Maintains user profiles and logs each drowsiness event with a timestamp
- ✅ Secured login/register system for personalized experience

---

## 🗂️ Project Structure

```
.
├── assets/                        # Audio & static assets
├── db/                            # SQLite databases for users and logs
├── modules/                       # Facial feature detection scripts
│   ├── EAR.py                     # Eye Aspect Ratio logic
│   ├── MAR.py                     # Mouth Aspect Ratio logic
│   ├── headpose.py                # Head pose detection (yaw)
├── app.py                         # Main Streamlit GUI
├── main.py                        # Drowsiness monitoring backend
├── notifier2.py                   # Email notifier
├── SQL.py                         # DB operations (login, events, contacts)
├── utils.py                       # Utility functions
├── requirements.txt               # Required packages
├── shape_predictor_68_face_landmarks.dat  # Dlib model for landmark detection
```

---

## 📥 Required File

👉 **Download:** [shape_predictor_68_face_landmarks.dat](https://github.com/italojs/facial-landmarks-recognition/blob/master/shape_predictor_68_face_landmarks.dat)  
After extracting, place the `.dat` file in your root directory.

This file is essential for facial landmark detection and must be included for the system to function properly.

---

## 🚦 How to Use

```bash
streamlit run app.py
```

Once launched, the app provides:
- 🔐 Login or registration page
- 👤 User detail & emergency contact form
- 👁️ Start Detection – Live monitoring with EAR, MAR & yaw tracking
- 📜 View logs of past drowsiness detection events

---

## ⚙️ System Features

### 🧍‍♂️ User Authentication
- Secure login and registration system
- Stores user details in a database

### 👨‍👩‍👧‍👦 Family Contact Management
- Add or update emergency contact details
- Used for sending alerts during drowsy states

### 👁️ Drowsiness Detection
- **EAR**: Detects eye closure duration
- **MAR**: Identifies yawning patterns
- **Yaw Angle**: Head pose estimation

### 🚨 Multi-level Alerts
- Plays audio warnings for short drowsiness
- Sends email alerts if drowsiness persists

### 🕒 Event Logging
- Timestamped records of every alert event
- View past logs in a tabular UI inside the app

---

## 🔧 Requirements

- Python 3.9
- dlib
- OpenCV
- Streamlit
- numpy
- scipy
- pandas
- imutils
- sqlite3 (builtin)
- smtplib (builtin)

---

## 👥 Project Credit

This project, DriCare360, was developed as a group academic submission.
While the collaboration involved shared ideas and planning, the complete implementation—including UI design, backend logic, feature integration —was independently carried out by Rupali Shewale.

