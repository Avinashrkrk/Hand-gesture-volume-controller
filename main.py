import cv2
import mediapipe as mp
import math
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
import numpy as np


class VolumeController:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7)
        self.mp_draw = mp.solutions.drawing_utils

        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        self.volume = interface.QueryInterface(IAudioEndpointVolume)
        vol_range = self.volume.GetVolumeRange()
        self.min_vol = vol_range[0]
        self.max_vol = vol_range[1]

        self.smooth_distance = 0
        self.mute = False

    def map_volume(self, distance):
        return np.interp(distance, [30, 200], [self.min_vol, self.max_vol])

    def toggle_mute(self, distance):
        if distance < 30 and not self.mute:
            self.mute = True
        elif distance >= 30 and self.mute:
            self.mute = False

    def draw_volume_bar(self, img, volume_level):
        h, w, _ = img.shape
        bar_x, bar_y = 50, int(h * 0.2)
        bar_height = int(h * 0.6)
        bar_width = 20

        cv2.rectangle(img, (bar_x, bar_y), (bar_x + bar_width, bar_y + bar_height), (200, 200, 200), 2)

        fill_height = int((1 - volume_level) * bar_height)
        color = (0, 255, 0) if not self.mute else (0, 0, 255)
        cv2.rectangle(img, (bar_x, bar_y + fill_height), (bar_x + bar_width, bar_y + bar_height), color, cv2.FILLED)

        percentage = "MUTED" if self.mute else f"{int(volume_level * 100)}%"
        cv2.putText(img, percentage, (bar_x + 30, bar_y + bar_height // 2),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)

    def process_frame(self, img):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.hands.process(img_rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(img, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)

                thumb_tip = hand_landmarks.landmark[4]
                index_tip = hand_landmarks.landmark[8]

                h, w, _ = img.shape
                x1, y1 = int(thumb_tip.x * w), int(thumb_tip.y * h)
                x2, y2 = int(index_tip.x * w), int(index_tip.y * h)

                cv2.circle(img, (x1, y1), 10, (255, 0, 255), cv2.FILLED)
                cv2.circle(img, (x2, y2), 10, (255, 0, 255), cv2.FILLED)
                cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 3)

                distance = math.hypot(x2 - x1, y2 - y1)
                self.smooth_distance = 0.8 * self.smooth_distance + 0.2 * distance

                self.toggle_mute(self.smooth_distance)

                if not self.mute:
                    vol = self.map_volume(self.smooth_distance)
                    self.volume.SetMasterVolumeLevel(vol, None)

                vol_percent = (vol - self.min_vol) / (self.max_vol - self.min_vol)

                self.draw_volume_bar(img, vol_percent)

        return img


def main():
    volume_controller = VolumeController()
    cap = cv2.VideoCapture(0)

    while True:
        success, img = cap.read()
        if not success:
            print("Failed to capture video.")
            break

        img = volume_controller.process_frame(img)

        cv2.imshow("Volume Control", img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
