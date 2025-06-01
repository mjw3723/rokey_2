import pyrealsense2 as rs
import cv2
import mediapipe as mp
import numpy as np

# MediaPipe 손 인식 초기화
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

# RealSense 파이프라인 초기화
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

pipeline.start(config)

try:
    while True:
        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        if not color_frame:
            continue

        color_image = np.asanyarray(color_frame.get_data())
        image_rgb = cv2.cvtColor(color_image, cv2.COLOR_BGR2RGB)
        results = hands.process(image_rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_draw.draw_landmarks(color_image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # 예: 검지 끝 (Landmark #8)
                index_tip = hand_landmarks.landmark[8]
                x = int(index_tip.x * color_image.shape[1])
                y = int(index_tip.y * color_image.shape[0])
                
                cv2.circle(color_image, (x, y), 8, (0, 255, 0), -1)


        cv2.imshow("RealSense + MediaPipe", color_image)
        if cv2.waitKey(1) & 0xFF == 27:
            break

finally:
    pipeline.stop()
    cv2.destroyA
