import cv2
import mediapipe as mp

class FaceTracker:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(static_image_mode=False,
                                                    max_num_faces=1,
                                                    min_detection_confidence=0.5,
                                                    min_tracking_confidence=0.5)

    def get_face_position_and_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return None, None

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(frame_rgb)

        if results.multi_face_landmarks:
            face_landmarks = results.multi_face_landmarks[0]
            nose_tip = face_landmarks.landmark[1]  # Index 1 typically corresponds to the nose tip
            frame_height, frame_width, _ = frame.shape
            nose_tip_y = int(nose_tip.y * frame_height)
            return nose_tip_y, frame
        else:
            return None, frame

    def release(self):
        self.cap.release()
        cv2.destroyAllWindows()
