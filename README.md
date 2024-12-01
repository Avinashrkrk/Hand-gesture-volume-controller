# Hand Gesture Volume Controller 🎛️  

A Python-based real-time volume control application that uses **hand gestures** captured via a webcam to adjust the system volume. This project leverages **OpenCV**, **Mediapipe**, and **PyCAW** for gesture detection and audio control.  

jfagfhg
flhajfh
---

## **Features**  
- **Real-Time Gesture Recognition**: Detects hand gestures using a webcam.  
- **Smooth Volume Control**: Adjusts system volume based on the distance between the thumb and index finger.  
- **Mute/Unmute Functionality**: Pinch gesture toggles mute/unmute state.  
- **Dynamic Volume Bar**: Displays current volume level visually on the screen.  

---

## **How It Works**  
1. **Gesture Detection**: Uses Mediapipe to identify hand landmarks.  
2. **Volume Adjustment**: Maps the distance between the thumb and index finger to the system volume range.  
3. **Mute/Unmute**: Detects pinch gestures to toggle the mute state.  
4. **UI Feedback**: Displays volume level or mute status on the screen.  

---

## **Technologies Used**  
- **Python**  
- **OpenCV**: For real-time video processing.  
- **Mediapipe**: For hand landmark detection.  
- **PyCAW**: For system volume control via Windows APIs.  

---

## **Installation**  

### **Prerequisites**  
- Python 3.7 or higher  
- Windows OS  

### **Steps**  
1. Clone the repository:  
   ```bash
   git clone https://github.com/yourusername/hand-gesture-volume-controller.git
   cd hand-gesture-volume-controller
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
3. Run the application:
   ```bash
   python main.py

## **Project Structure**
```bash
hand-gesture-volume-controller/
│
├── volume_controller.py    # Main application script
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
```
## **Usage**
1. Ensure your webcam is connected.
2. Run the script.
3. Use the following gestures:
   -Move your thumb and index finger closer or apart to adjust the volume.
   -Pinch your fingers together to toggle mute/unmute.

