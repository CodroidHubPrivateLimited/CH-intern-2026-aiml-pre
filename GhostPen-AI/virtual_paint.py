import cv2
import mediapipe as mp
import numpy as np
import time

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

canvas = np.zeros((480, 640, 3), dtype=np.uint8)

prev_x, prev_y = 0, 0
color = (255, 0, 0)

# Smooth drawing
alpha = 0.5
smooth_x, smooth_y = 0, 0

# Save popup
show_saved = False
saved_time = 0

# Mode tracking
mode = "Idle"

colors = [(255,0,0),(0,255,0),(0,0,255)]
selected_index = 0

while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)

    overlay = frame.copy()

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    #  TOP BAR BACKGROUND
    cv2.rectangle(overlay, (0, 0), (640, 70), (50, 50, 50), -1)
    frame = cv2.addWeighted(overlay, 0.6, frame, 0.4, 0)

    #  COLOR BUTTONS
    for i, col in enumerate(colors):
        x1 = 20 + i*80
        x2 = x1 + 60

        cv2.rectangle(frame, (x1, 10), (x2, 60), col, -1)

        if i == selected_index:
            cv2.rectangle(frame, (x1-3, 7), (x2+3, 63), (255,255,255), 2)

    # CLEAR BUTTON
    cv2.rectangle(frame, (300, 10), (380, 60), (0, 0, 0), -1)
    cv2.putText(frame, "CLEAR", (305, 45),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2)

    # SAVE BUTTON
    cv2.rectangle(frame, (400, 10), (480, 60), (200, 200, 200), -1)
    cv2.putText(frame, "SAVE", (415, 45),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,0), 2)

    # TITLE
    cv2.putText(frame, "AI Writing System",
                (180, 460),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)

    if result.multi_hand_landmarks:
        for hand in result.multi_hand_landmarks:

            h, w, _ = frame.shape
            x = int(hand.landmark[8].x * w)
            y = int(hand.landmark[8].y * h)

            # Smooth movement
            smooth_x = int(alpha * x + (1-alpha)*smooth_x)
            smooth_y = int(alpha * y + (1-alpha)*smooth_y)

            # Cursor
            cv2.circle(frame, (smooth_x, smooth_y), 8, (255,255,255), -1)

            index_up = hand.landmark[8].y < hand.landmark[6].y
            middle_up = hand.landmark[12].y < hand.landmark[10].y

            #  Selection Mode
            if index_up and middle_up:
                mode = "Selection Mode"
                prev_x, prev_y = 0, 0

                if smooth_y < 70:

                    # Color selection
                    for i in range(len(colors)):
                        if 20 + i*80 < smooth_x < 80 + i*80:
                            color = colors[i]
                            selected_index = i

                    # Clear
                    if 300 < smooth_x < 380:
                        canvas = np.zeros((480, 640, 3), dtype=np.uint8)

                    # Save
                    if 400 < smooth_x < 480:
                        filename = f"drawing_{int(time.time())}.png"
                        cv2.imwrite(filename, canvas)
                        show_saved = True
                        saved_time = time.time()

            #  Write Mode
            elif index_up and not middle_up:
                mode = "Write Mode"

                if prev_x == 0 and prev_y == 0:
                    prev_x, prev_y = smooth_x, smooth_y

                cv2.line(canvas,
                         (prev_x, prev_y),
                         (smooth_x, smooth_y),
                         color, 6)

                prev_x, prev_y = smooth_x, smooth_y

            #  Erase Mode
            elif not index_up and not middle_up:
                mode = "Erase Mode"

                cv2.circle(canvas, (smooth_x, smooth_y), 20, (0, 0, 0), -1)
                prev_x, prev_y = 0, 0

            else:
                mode = "Idle"
                prev_x, prev_y = 0, 0

            mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)

    #  SAVE POPUP
    if show_saved:
        cv2.rectangle(frame, (200, 200), (440, 280), (0, 0, 0), -1)
        cv2.putText(frame, "Saved Successfully!",
                    (220, 250),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)

        if time.time() - saved_time > 2:
            show_saved = False

    # Merge canvas
    gray = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(gray, 20, 255, cv2.THRESH_BINARY)
    mask_inv = cv2.bitwise_not(mask)

    frame_bg = cv2.bitwise_and(frame, frame, mask=mask_inv)
    canvas_fg = cv2.bitwise_and(canvas, canvas, mask=mask)

    final = cv2.add(frame_bg, canvas_fg)

    #  MODE DISPLAY BOX
    cv2.rectangle(final, (430, 400), (630, 460), (0, 0, 0), -1)

    if mode == "Write Mode":
        color_text = (0, 255, 0)
    elif mode == "Erase Mode":
        color_text = (0, 0, 255)
    elif mode == "Selection Mode":
        color_text = (255, 255, 0)
    else:
        color_text = (200, 200, 200)

    cv2.putText(final, mode,
                (440, 440),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7, color_text, 2)

    cv2.imshow("AI Virtual Writing System - Pro", final)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()