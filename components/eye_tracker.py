import cv2
import mediapipe as mp
import pyautogui
import math


def calculate_eye_aspect_ratio(eye_points):
    vertical_distance_1 = math.dist(eye_points[1], eye_points[5])
    vertical_distance_2 = math.dist(eye_points[2], eye_points[4])
    horizontal_distance = math.dist(eye_points[0], eye_points[3])
    ear = (vertical_distance_1 + vertical_distance_2) / (2.0 * horizontal_distance)
    return ear


def map_eye_to_screen(avg_eye_x, avg_eye_y, cam_w, cam_h, screen_w, screen_h, sensitivity=2.0):
    cam_center_x, cam_center_y = cam_w / 2, cam_h / 2
    offset_x = avg_eye_x - cam_center_x
    offset_y = avg_eye_y - cam_center_y
    scale_x = screen_w / cam_w
    scale_y = screen_h / cam_h
    screen_center_x, screen_center_y = screen_w / 2, screen_h / 2
    new_x = screen_center_x - int(offset_x * sensitivity * scale_x)
    new_y = screen_center_y + int(offset_y * sensitivity * scale_y)
    new_x = min(max(new_x, 0), screen_w)
    new_y = min(max(new_y, 0), screen_h)
    return new_x, new_y


def run_eye_tracker() -> None:
    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.5,
                                      min_tracking_confidence=0.5)
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    LEFT_EYE_INDICES = [33, 160, 158, 133, 153, 144]
    RIGHT_EYE_INDICES = [362, 385, 387, 263, 373, 380]
    screen_width, screen_height = pyautogui.size()
    sensitivity = 2.0

    # Blink detection settings
    ear_threshold = 0.2
    consecutive_frame_threshold = 3  # number of consecutive frames required to register a blink
    blink_counter = 0

    prev_x, prev_y = pyautogui.position()

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        h, w, _ = frame.shape
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb_frame)

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                left_eye_points = [(int(face_landmarks.landmark[i].x * w),
                                    int(face_landmarks.landmark[i].y * h))
                                   for i in LEFT_EYE_INDICES]
                right_eye_points = [(int(face_landmarks.landmark[i].x * w),
                                     int(face_landmarks.landmark[i].y * h))
                                    for i in RIGHT_EYE_INDICES]

                left_eye_center = (sum(p[0] for p in left_eye_points) // len(left_eye_points),
                                   sum(p[1] for p in left_eye_points) // len(left_eye_points))
                right_eye_center = (sum(p[0] for p in right_eye_points) // len(right_eye_points),
                                    sum(p[1] for p in right_eye_points) // len(right_eye_points))

                # Calculate EAR for each eye and take the minimum
                left_ear = calculate_eye_aspect_ratio(left_eye_points)
                right_ear = calculate_eye_aspect_ratio(right_eye_points)
                min_ear = min(left_ear, right_ear)

            avg_eyes_x = (left_eye_center[0] + right_eye_center[0]) / 2
            avg_eyes_y = (left_eye_center[1] + right_eye_center[1]) / 2
            mapped_x, mapped_y = map_eye_to_screen(avg_eyes_x, avg_eyes_y, w, h,
                                                   screen_width, screen_height,
                                                   sensitivity=sensitivity)
            pyautogui.moveTo(mapped_x, mapped_y)

            # Check blink over consecutive frames using the minimum EAR
            if min_ear < ear_threshold:
                blink_counter += 1
            else:
                blink_counter = 0

            if blink_counter >= consecutive_frame_threshold:
                pyautogui.leftClick(mapped_x, mapped_y)
                blink_counter = 0  # Reset after registering a blink

        else:
            pyautogui.moveTo(prev_x, prev_y)

        prev_x, prev_y = pyautogui.position()

    cap.release()
    cv2.destroyAllWindows()
